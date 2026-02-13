#!/usr/bin/env python3
"""
acord_filler — Programmatically fill ACORD 125/140 insurance forms.

CLI:
    python acord_filler.py --input data.json --form blank.pdf --output filled.pdf
    python acord_filler.py --form blank.pdf --list-fields

Library:
    from acord_filler import fill_acord
    result = fill_acord("blank.pdf", "data.json", "filled.pdf")

Built by Alliance Risk Insurance Services LLC.
MIT License.
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
from datetime import date
from typing import Any, Optional

import fitz  # PyMuPDF

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# General Info Y/N overlay coordinates (page 3, 0-indexed page 2).
# These checkboxes don't accept text via widget API, so we draw text after
# flattening. Each tuple: (field_name, x_yes, x_no, y).
GENERAL_INFO_YN_COORDS = [
    ("ACORD_General_CoverageTerminated", 498, 524, 164),
    ("ACORD_General_Subsidiary", 498, 524, 179),
    ("ACORD_General_Parent", 498, 524, 194),
    ("ACORD_General_OtherVentures", 498, 524, 232),
    ("ACORD_General_Exposure", 498, 524, 247),
    ("ACORD_General_Foreign", 498, 524, 262),
    ("ACORD_General_Trust", 498, 524, 277),
    ("ACORD_General_OtherInsurance", 498, 524, 315),
    ("ACORD_General_PossessDrones", 498, 524, 353),
    ("ACORD_General_HireDrones", 498, 524, 368),
    ("ACORD_General_IndictedOrConvicted", 498, 524, 406),
    ("ACORD_General_SafetyViolations", 498, 524, 421),
    ("ACORD_General_NegativeFinancialAction", 498, 524, 459),
    ("ACORD_General_JudgementLien", 498, 524, 474),
    ("ACORD_General_Safety", 498, 524, 512),
    ("ACORD_General_PastAllegations", 498, 524, 550),
]

# Prior carrier Property column x-offset. The form field names say "Auto"
# but the columns are generic. We draw Property values at this x position.
PRIOR_CARRIER_PROPERTY_X = 355

# Prior carrier row y-coordinates (page 3) for rows 1-3
PRIOR_CARRIER_ROWS = {
    1: {"carrier": 614, "policy": 629, "premium": 644, "eff": 659, "exp": 674},
    2: {"carrier": 614, "policy": 629, "premium": 644, "eff": 659, "exp": 674},
    3: {"carrier": 614, "policy": 629, "premium": 644, "eff": 659, "exp": 674},
}

# ACORD 140 Section A (page 9) row letters and Section B (page 10) row letters
SECTION_A_ROWS = ["A", "B", "C", "D", "E"]  # Location 1
SECTION_B_ROWS = ["G", "H", "I", "J", "K"]  # Location 2

# Pages to skip for property-only policies (GL pages, 0-indexed)
GL_PAGE_INDICES = [4, 5, 6, 7]  # Pages 5-8 (GL section)


# ---------------------------------------------------------------------------
# Core functions
# ---------------------------------------------------------------------------


def list_fields(form_path: str) -> dict[str, dict]:
    """List all fillable fields in an ACORD PDF.

    Returns:
        Dict mapping field_name -> {page, type, value}
    """
    doc = fitz.open(form_path)
    fields = {}
    for page_num, page in enumerate(doc):
        for widget in page.widgets():
            fields[widget.field_name] = {
                "page": page_num + 1,
                "type": widget.field_type_string,
                "value": widget.field_value or "",
            }
    doc.close()
    return fields


def _build_field_data(config: dict) -> dict[str, str]:
    """Transform a high-level JSON config into flat field_name:value pairs.

    Handles the mapping from structured location/coverage data to the actual
    ACORD field names (which are often non-obvious).
    """
    fields: dict[str, str] = {}

    # --- Direct top-level fields ---
    # These keys in the config match ACORD field names directly.
    direct_keys = [
        "ACORD_AgencyName",
        "ACORD_CarrierName",
        "ACORD_PolicyNumber",
        "ACORD_Policy_EffectiveDate",
        "ACORD_Policy_ExpirationDate",
        "ACORD_Policy_Insured1_Name",
        "ACORD_Policy_Insured1_MailingAddress",
        "ACORD_Policy_Insured1_SIC",
        "ACORD_Policy_Insured1_PhoneNumber",
        "ACORD_Policy_Insured1_FEINSSN",
        "ACORD_Policy_Insured1_Website",
        "ACORD_Policy_PolicyPremium",
        "ACORD_NAICCode",
        "ACORD_NatureOfBusiness_Description",
        "ACORD_ProducerContact",
        "ACORD_ProducerPhoneNumber",
        "ACORD_ProducerEmailAddress",
        "ACORD_ProducerCode",
    ]
    for key in direct_keys:
        if key in config:
            fields[key] = str(config[key])

    # Auto-populate date fields
    today = config.get("_override_date", date.today().strftime("%m/%d/%Y"))
    fields["ACORD_CurrentDate"] = today
    fields["ACORD_Transaction_Date"] = today

    # --- Transaction type checkboxes ---
    tx = config.get("transaction_type", "quote")
    tx_map = {
        "quote": "ACORD_Transaction_Quote",
        "bound": "ACORD_Transaction_Bound",
        "renew": "ACORD_Transaction_Renew",
        "cancel": "ACORD_Transaction_Cancel",
        "change": "ACORD_Transaction_Change",
        "issue": "ACORD_Transaction_IssuePolicy",
    }
    if tx in tx_map:
        fields[tx_map[tx]] = "Yes"

    # --- Entity type checkbox ---
    entity = config.get("entity_type", "").lower()
    entity_map = {
        "llc": "ACORD_Policy_Insured1_Type_LLC",
        "corporation": "ACORD_Policy_Insured1_Type_Corporation",
        "partnership": "ACORD_Policy_Insured1_Type_Partnership",
        "individual": "ACORD_Policy_Insured1_Type_Individual",
        "scorp": "ACORD_Policy_Insured1_Type_SCorp",
        "trust": "ACORD_Policy_Insured1_Type_Trust",
        "joint_venture": "ACORD_Policy_Insured1_Type_JointVenture",
    }
    if entity in entity_map:
        fields[entity_map[entity]] = "Yes"

    # --- Locations (Page 2 - ACORD 125) ---
    locations = config.get("locations", {})
    loc_keys = sorted(locations.keys())  # e.g., ["loc1", "loc2"]

    for i, loc_key in enumerate(loc_keys[:4]):  # Max 4 locations on page 2
        loc = locations[loc_key]
        n = i + 1  # 1-indexed
        prefix = f"ACORD_Location{n}_"

        if "address" in loc:
            # Parse address: "street, city, ST ZIP"
            parts = loc["address"].split(",")
            if len(parts) >= 3:
                fields[f"{prefix}Street"] = parts[0].strip()
                fields[f"{prefix}City"] = parts[1].strip()
                st_zip = parts[2].strip().split()
                if st_zip:
                    fields[f"{prefix}State"] = st_zip[0]
                if len(st_zip) > 1:
                    fields[f"{prefix}ZIP"] = st_zip[1]

        if "county" in loc:
            fields[f"{prefix}County"] = loc["county"]
        if "description" in loc:
            fields[f"{prefix}Description"] = loc["description"]
        if "sqft" in loc:
            fields[f"{prefix}BuildingArea"] = str(loc["sqft"])
            fields[f"{prefix}OccupiedArea"] = str(loc["sqft"])
        if "premises" in loc:
            fields[f"{prefix}LocationNumber"] = str(loc["premises"])
        if "building" in loc:
            fields[f"{prefix}BuildingNumber"] = str(loc["building"])

        # Interest checkboxes
        interest = loc.get("interest", "owner").lower()
        if interest == "owner":
            fields[f"{prefix}Interest_Owner"] = "Yes"
        elif interest == "tenant":
            fields[f"{prefix}Interest_Tenant"] = "Yes"

    # --- ACORD 140 Property Section (Pages 9-10) ---
    for i, loc_key in enumerate(loc_keys[:2]):  # Max 2 on ACORD 140
        loc = locations[loc_key]
        suffix = "A" if i == 0 else "B"
        row_letters = SECTION_A_ROWS if i == 0 else SECTION_B_ROWS

        # Header fields
        fields[f"CommercialStructure_Location_ProducerIdentifier_{suffix}"] = str(
            loc.get("premises", i + 1)
        )
        fields[f"CommercialStructure_Building_ProducerIdentifier_{suffix}"] = str(
            loc.get("building", 1)
        )
        fields[f"CommercialStructure_PhysicalAddress_LineOne_{suffix}"] = loc.get(
            "address", ""
        )
        fields[
            f"CommercialStructure_Building_SublocationDescription_{suffix}"
        ] = loc.get("description", "")

        # Construction details
        if "construction" in loc:
            fields[f"Construction_ConstructionCode_{suffix}"] = loc["construction"]
        if "year_built" in loc:
            fields[f"CommercialStructure_BuiltYear_{suffix}"] = str(loc["year_built"])
        if "stories" in loc:
            fields[f"Construction_StoreyCount_{suffix}"] = str(loc["stories"])
        if "basements" in loc:
            fields[f"Construction_BasementCount_{suffix}"] = str(loc["basements"])
        if "sqft" in loc:
            fields[f"Construction_BuildingArea_{suffix}"] = str(loc["sqft"])
        if "roof" in loc:
            fields[f"Construction_RoofMaterialCode_{suffix}"] = loc["roof"]
        if "protection_class" in loc:
            fields[
                f"BuildingFireProtection_ProtectionClassCode_{suffix}"
            ] = loc["protection_class"]

        # Exposures
        exposures = loc.get("exposures", {})
        for direction in ["front", "rear", "left", "right"]:
            exp = exposures.get(direction, {})
            if exp:
                cap = direction.capitalize()
                if "desc" in exp:
                    fields[f"BuildingExposure_{cap}Description_{suffix}"] = exp["desc"]
                if "dist" in exp:
                    fields[f"BuildingExposure_{cap}Distance_{suffix}"] = exp["dist"]

        # Coverage row (first row of section)
        row = row_letters[0]
        if "limit" in loc:
            fields[f"CommercialProperty_Premises_LimitAmount_{row}"] = str(loc["limit"])
        if "coinsurance" in loc:
            fields[f"CommercialProperty_Premises_CoinsurancePercent_{row}"] = str(
                loc["coinsurance"]
            )
        if "valuation" in loc:
            fields[f"CommercialProperty_Premises_ValuationCode_{row}"] = loc[
                "valuation"
            ]
        if "cause_of_loss" in loc:
            fields[f"CommercialProperty_Premises_CauseOfLossCode_{row}"] = loc[
                "cause_of_loss"
            ]
        if "deductible" in loc:
            fields[f"CommercialProperty_Premises_DeductibleAmount_{row}"] = str(
                loc["deductible"]
            )
        if "ded_type" in loc:
            fields[f"CommercialProperty_Premises_DeductibleTypeCode_{row}"] = loc[
                "ded_type"
            ]
        if "subject_of_insurance" in loc:
            fields[f"CommercialProperty_Premises_SubjectOfInsuranceCode_{row}"] = loc[
                "subject_of_insurance"
            ]

        # Mine subsidence / sinkhole (Texas defaults)
        state = loc.get("state", "")
        if not state and "address" in loc:
            parts = loc["address"].split(",")
            if len(parts) >= 3:
                st_zip = parts[2].strip().split()
                if st_zip:
                    state = st_zip[0]

        if state == "TX":
            fields[
                f"CommercialPropertyCoverage_MineSubsidenceOption_NoIndicator_{suffix}"
            ] = "Yes"
            fields[
                f"CommercialPropertyCoverage_SinkHoleCollapse_NoIndicator_{suffix}"
            ] = "Yes"

        # Equipment breakdown
        if loc.get("equipment_breakdown"):
            fields[
                f"CommercialProperty_Premises_BreakdownOrContaminationIndicator_{suffix}"
            ] = "Yes"

    # --- ACORD 140 header fields ---
    if loc_keys:
        loc1 = locations[loc_keys[0]]
        fields["NamedInsured_FullName_A"] = config.get(
            "ACORD_Policy_Insured1_Name", ""
        )
        fields["Policy_PolicyNumberIdentifier_A"] = config.get(
            "ACORD_PolicyNumber", ""
        )
        fields["Policy_EffectiveDate_A"] = config.get(
            "ACORD_Policy_EffectiveDate", ""
        )
        fields["Insurer_FullName_A"] = config.get("ACORD_CarrierName", "")
        fields["Producer_FullName_A"] = config.get("ACORD_AgencyName", "").split("\n")[
            0
        ]
        fields["Form_CompletionDate_A"] = today

    # --- Prior carrier (fill "Auto" fields — Property column drawn manually) ---
    prior = config.get("prior_carrier", {})
    if prior:
        row_num = 1
        prefix = f"ACORD_PriorCarrier_{row_num}_Auto"
        # We fill the Auto fields since they're the only widget fields available.
        # The Property column values will be drawn manually at x:355.
        fields[f"{prefix}Carrier"] = prior.get("carrier", "")
        fields[f"{prefix}PolicyNumber"] = prior.get("policy_number", "")
        fields[f"{prefix}Premium"] = prior.get("premium", "")
        fields[f"{prefix}EffectiveDate"] = prior.get("effective", "")
        fields[f"{prefix}ExpirationDate"] = prior.get("expiration", "")

    # --- Loss history ---
    if config.get("loss_history_none", True):
        fields["ACORD_LossHistory_None"] = "Yes"

    losses = config.get("loss_history", [])
    for i, loss in enumerate(losses[:3]):  # Max 3 rows
        n = i + 1
        prefix = f"ACORD_LossHistory_{n}_"
        for key in [
            "DateOfClaim",
            "OccurenceDate",
            "Description",
            "LOB",
            "AmountPaid",
            "AmountReserved",
            "ClaimOpen",
            "Subrogation",
        ]:
            if key.lower() in loss or key in loss:
                fields[f"{prefix}{key}"] = str(loss.get(key, loss.get(key.lower(), "")))

    # --- Checkboxes ---
    checkboxes = config.get("checkboxes", {})
    for field_name, value in checkboxes.items():
        fields[field_name] = "Yes" if value else ""

    # --- Any additional raw field overrides ---
    overrides = config.get("field_overrides", {})
    fields.update(overrides)

    return fields


def _fill_widgets(doc: fitz.Document, fields: dict[str, str]) -> tuple[int, list[str]]:
    """Fill PDF form widgets with field data.

    Returns:
        (filled_count, list of skipped field names not found in form)
    """
    all_field_names = set()
    filled = 0

    for page in doc:
        for widget in page.widgets():
            all_field_names.add(widget.field_name)
            if widget.field_name in fields:
                widget.field_value = str(fields[widget.field_name])
                widget.update()
                filled += 1

    skipped = [k for k in fields if k not in all_field_names]
    return filled, skipped


def _flatten_to_images(doc: fitz.Document, output_path: str, dpi: int = 200) -> None:
    """Flatten PDF by rendering each page as an image and rebuilding."""
    dst = fitz.open()
    for page in doc:
        pix = page.get_pixmap(dpi=dpi)
        img_page = dst.new_page(width=page.rect.width, height=page.rect.height)
        img_page.insert_image(page.rect, pixmap=pix)
    dst.save(output_path, deflate=True)
    dst.close()


def _draw_general_info_yn(
    doc: fitz.Document, config: dict, page_index: int = 2
) -> None:
    """Draw Y/N text overlays for General Info checkboxes.

    These checkbox widgets don't accept text, so we draw directly on the
    flattened image page.
    """
    if page_index >= len(doc):
        return

    page = doc[page_index]
    all_no = config.get("general_info_all_no", False)
    yn_overrides = config.get("general_info", {})

    for field_name, x_yes, x_no, y in GENERAL_INFO_YN_COORDS:
        short = field_name.replace("ACORD_General_", "")
        value = yn_overrides.get(short, "N" if all_no else "")
        if not value:
            continue

        x = x_yes if value.upper() == "Y" else x_no
        page.insert_text(
            (x, y),
            value.upper(),
            fontsize=8,
            fontname="helv",
            color=(0, 0, 0),
        )


def _draw_prior_carrier_property(
    doc: fitz.Document, config: dict, page_index: int = 2
) -> None:
    """Draw prior carrier Property column values at x:355.

    The ACORD form field names say 'Auto' but the columns are generic.
    We draw Property values manually since there are no dedicated fields.
    """
    prior = config.get("prior_carrier", {})
    if not prior or page_index >= len(doc):
        return

    page = doc[page_index]
    # Y positions for prior carrier property column on page 3
    # These are approximate — adjust based on your specific form version
    y_positions = {
        "carrier": 614,
        "policy_number": 629,
        "premium": 644,
        "effective": 659,
        "expiration": 674,
    }

    for key, y in y_positions.items():
        value = prior.get(key, "")
        if value:
            page.insert_text(
                (PRIOR_CARRIER_PROPERTY_X, y),
                str(value),
                fontsize=7,
                fontname="helv",
                color=(0, 0, 0),
            )


def _apply_ocr(pdf_path: str) -> bool:
    """Apply OCR to a flattened PDF using ocrmypdf.

    Returns True if successful, False otherwise.
    """
    try:
        subprocess.run(
            [
                "ocrmypdf",
                "--skip-text",
                "--optimize", "1",
                "--output-type", "pdf",
                pdf_path,
                pdf_path,
            ],
            check=True,
            capture_output=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Warning: OCR failed ({e}). Output is image-only.", file=sys.stderr)
        return False


def _create_broker_notes_pdf(notes: list[str], output_path: str) -> None:
    """Create a standalone broker notes PDF.

    Broker notes contain valuation flags, coverage gaps, and underwriting
    observations. These NEVER go on the signed ACORD application.
    """
    doc = fitz.open()
    page = doc.new_page(width=612, height=792)

    # Title
    page.insert_text(
        (50, 50),
        "BROKER NOTES — VALUATION & COVERAGE FLAGS",
        fontsize=14,
        fontname="helv",
        color=(0.2, 0.2, 0.6),
    )
    page.insert_text(
        (50, 68),
        "CONFIDENTIAL — Not part of the signed application",
        fontsize=8,
        fontname="helv",
        color=(0.5, 0.5, 0.5),
    )

    y = 90
    for i, note in enumerate(notes, 1):
        # Word-wrap and calculate box height
        words = note.split()
        lines = []
        line = ""
        for w in words:
            test = f"{line} {w}" if line else w
            if len(test) > 85:
                lines.append(line)
                line = w
            else:
                line = test
        if line:
            lines.append(line)

        box_height = 20 + len(lines) * 12 + 8

        # Page break check
        if y + box_height > 750:
            page = doc.new_page(width=612, height=792)
            y = 50

        # Amber background
        rect = fitz.Rect(40, y, 572, y + box_height)
        page.draw_rect(
            rect, color=(0.8, 0.6, 0.1), fill=(1.0, 0.95, 0.85), width=0.5
        )

        # Note text
        ty = y + 14
        for ln in lines:
            page.insert_text(
                (48, ty), ln, fontsize=8, fontname="helv", color=(0.2, 0.2, 0.2)
            )
            ty += 12

        y += box_height + 6

    doc.save(output_path, deflate=True)
    doc.close()


def fill_acord(
    form_path: str,
    input_path: str,
    output_path: str,
    flatten: bool = True,
    ocr: bool = False,
    dpi: int = 200,
    broker_notes_path: Optional[str] = None,
    skip_gl: bool = False,
) -> dict[str, Any]:
    """Fill an ACORD 125/140 form from a JSON config file.

    Args:
        form_path: Path to blank fillable ACORD PDF.
        input_path: Path to JSON config file.
        output_path: Where to save the filled PDF.
        flatten: Render to non-editable image PDF (default True).
        ocr: Apply OCR for searchable text (default False).
        dpi: Resolution for flattening (default 200).
        broker_notes_path: If set, write broker notes to this separate PDF.
        skip_gl: Skip GL pages (5-8) for property-only policies.

    Returns:
        Dict with filled_count, total_fields, skipped_fields, ocr_applied.
    """
    with open(input_path) as f:
        config = json.load(f)

    # Build flat field mapping from structured config
    fields = _build_field_data(config)

    # Open form and fill widgets
    doc = fitz.open(form_path)
    filled_count, skipped = _fill_widgets(doc, fields)
    total_fields = sum(1 for p in doc for _ in p.widgets())

    if flatten:
        # Save temp filled version, then flatten
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp_path = tmp.name
        doc.save(tmp_path)
        doc.close()

        # Re-open and flatten to images
        src = fitz.open(tmp_path)

        if skip_gl:
            # Remove GL pages before flattening
            pages_to_keep = [
                i for i in range(len(src)) if i not in GL_PAGE_INDICES
            ]
            dst = fitz.open()
            for i in pages_to_keep:
                page = src[i]
                pix = page.get_pixmap(dpi=dpi)
                img_page = dst.new_page(width=page.rect.width, height=page.rect.height)
                img_page.insert_image(page.rect, pixmap=pix)
        else:
            dst = fitz.open()
            for page in src:
                pix = page.get_pixmap(dpi=dpi)
                img_page = dst.new_page(
                    width=page.rect.width, height=page.rect.height
                )
                img_page.insert_image(page.rect, pixmap=pix)

        src.close()
        os.unlink(tmp_path)

        # Draw overlays on flattened pages
        _draw_general_info_yn(dst, config, page_index=2)
        _draw_prior_carrier_property(dst, config, page_index=2)

        dst.save(output_path, deflate=True)
        dst.close()
    else:
        doc.save(output_path)
        doc.close()

    # OCR
    ocr_applied = False
    if ocr and flatten:
        ocr_applied = _apply_ocr(output_path)

    # Broker notes (always a separate file)
    notes = config.get("broker_notes", [])
    if broker_notes_path and notes:
        _create_broker_notes_pdf(notes, broker_notes_path)

    return {
        "filled_count": filled_count,
        "total_fields": total_fields,
        "skipped_fields": skipped,
        "ocr_applied": ocr_applied,
        "output_path": output_path,
        "broker_notes_path": broker_notes_path if notes else None,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Fill ACORD 125/140 insurance forms from JSON data.",
        epilog="Built by Alliance Risk Insurance Services LLC. MIT License.",
    )
    parser.add_argument(
        "--input", "-i", help="JSON config file with form data"
    )
    parser.add_argument(
        "--form", "-f", required=True, help="Path to blank ACORD PDF"
    )
    parser.add_argument(
        "--output", "-o", help="Output PDF path"
    )
    parser.add_argument(
        "--no-flatten",
        action="store_true",
        help="Keep output editable (don't flatten)",
    )
    parser.add_argument(
        "--ocr", action="store_true", help="Apply OCR for searchable text"
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=200,
        help="DPI for flattening (default: 200)",
    )
    parser.add_argument(
        "--broker-notes",
        help="Output path for separate broker notes PDF",
    )
    parser.add_argument(
        "--skip-gl",
        action="store_true",
        help="Skip GL pages (property-only policy)",
    )
    parser.add_argument(
        "--list-fields",
        action="store_true",
        help="List all field names in the blank form and exit",
    )

    args = parser.parse_args()

    # List fields mode
    if args.list_fields:
        fields = list_fields(args.form)
        print(f"Total fields: {len(fields)}\n")
        for name in sorted(fields.keys()):
            f = fields[name]
            print(f"  Page {f['page']:2d} | {f['type']:10s} | {name}")
        return

    # Fill mode requires input and output
    if not args.input or not args.output:
        parser.error("--input and --output are required for filling")

    result = fill_acord(
        form_path=args.form,
        input_path=args.input,
        output_path=args.output,
        flatten=not args.no_flatten,
        ocr=args.ocr,
        dpi=args.dpi,
        broker_notes_path=args.broker_notes,
        skip_gl=args.skip_gl,
    )

    print(f"Filled {result['filled_count']} of {result['total_fields']} fields")
    if result["skipped_fields"]:
        print(f"Skipped (not in form): {', '.join(result['skipped_fields'][:10])}")
        if len(result["skipped_fields"]) > 10:
            print(f"  ... and {len(result['skipped_fields']) - 10} more")
    if result["ocr_applied"]:
        print("OCR applied ✓")
    print(f"Saved to {result['output_path']}")
    if result["broker_notes_path"]:
        print(f"Broker notes saved to {result['broker_notes_path']}")


if __name__ == "__main__":
    main()
