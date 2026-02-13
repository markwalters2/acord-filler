#!/usr/bin/env python3
"""
ACORD 37 (Statement of No Loss) Filler
Uses PyMuPDF (fitz) to fill the standard ACORD 37 form.

Usage:
    python fill_acord37.py --input data.json --form acord-37-blank.pdf --output filled.pdf

Input JSON schema:
{
    "agency_name": "Agency Name",
    "agency_address_1": "Street Address",
    "agency_address_2": "City, State ZIP",
    "agency_code": "",
    "agency_subcode": "",
    "contact_name": "Contact Person",
    "phone": "(555) 555-5555",
    "fax": "",
    "email": "email@example.com",
    "insured_name": "Named Insured LLC",
    "insured_address": "123 Main St, City, ST 00000",
    "carrier": "Insurance Carrier Name",
    "naic_code": "12345",
    "policy_number": "POL-000000",
    "approved_by": "Approver Name",
    "from_date": "MM/DD/YYYY",
    "to_date": "MM/DD/YYYY",
    "cancellation_date": "MM/DD/YYYY",
    "applicant_name": "Signatory Name / Title",
    "date_signed": "MM/DD/YYYY"
}
"""

import fitz
import json
import argparse
import subprocess
import os
from datetime import date


# Field name -> JSON key mapping
FIELD_MAP = {
    "F[0].P1[0].Text1[0]":  "agency_name",
    "F[0].P1[0].Text2[0]":  "agency_address_1",
    "F[0].P1[0].Text3[0]":  "agency_address_2",
    "F[0].P1[0].Text4[0]":  "agency_code",
    "F[0].P1[0].Text5[0]":  "agency_subcode",
    "F[0].P1[0].Text7[0]":  "contact_name",
    "F[0].P1[0].Text8[0]":  "phone",
    "F[0].P1[0].Text9[0]":  "fax",
    "F[0].P1[0].Text10[0]": "email",
    "F[0].P1[0].Text13[0]": "agency_customer_id",
    "F[0].P1[0].Text14[0]": "insured_name",
    "F[0].P1[0].Text15[0]": "insured_name_2",
    "F[0].P1[0].Text16[0]": "insured_address",
    "F[0].P1[0].Text17[0]": "insured_address_2",
    "F[0].P1[0].Text18[0]": "carrier",
    "F[0].P1[0].Text19[0]": "naic_code",
    "F[0].P1[0].Text20[0]": "policy_number",
    "F[0].P1[0].Text21[0]": "approved_by",
    "F[0].P1[0].Text22[0]": "from_date",
    "F[0].P1[0].Text23[0]": "to_date",
    "F[0].P1[0].Text24[0]": "cancellation_date",
    "F[0].P1[0].Text25[0]": "applicant_name",
    "F[0].P1[0].Text26[0]": "receipt_amount",
    "F[0].P1[0].Text27[0]": "received_by",
    "F[0].P1[0].Text28[0]": "witness",
    "F[0].P1[0].Text29[0]": "witness_date",
    "F[0].P1[0].Text30[0]": "receipt_date",
}


def fill_acord37(data: dict, form_path: str, output_path: str, ocr: bool = True):
    """Fill an ACORD 37 Statement of No Loss form.
    
    Args:
        data: Dictionary with form field values
        form_path: Path to blank ACORD 37 PDF
        output_path: Path for output PDF
        ocr: Whether to add OCR text layer (requires ocrmypdf + tesseract)
    
    Returns:
        dict with fill stats
    """
    doc = fitz.open(form_path)
    filled = 0

    for widget in doc[0].widgets():
        fname = widget.field_name
        if fname in FIELD_MAP:
            key = FIELD_MAP[fname]
            value = data.get(key, "")
            if value:
                widget.field_value = str(value)
                widget.update()
                filled += 1

    # Flatten: render as image, rebuild
    pix = doc[0].get_pixmap(dpi=200)
    dst = fitz.open()
    page = dst.new_page(width=doc[0].rect.width, height=doc[0].rect.height)
    page.insert_image(doc[0].rect, pixmap=pix)
    doc.close()

    # Save flattened
    if ocr:
        tmp_path = output_path + ".tmp.pdf"
        dst.save(tmp_path, deflate=True)
        dst.close()
        try:
            subprocess.run(
                ["ocrmypdf", "--skip-text", "--optimize", "1", tmp_path, output_path],
                capture_output=True, text=True, timeout=60
            )
            os.remove(tmp_path)
        except (FileNotFoundError, subprocess.TimeoutExpired):
            # ocrmypdf not available, use unOCR'd version
            os.rename(tmp_path, output_path)
    else:
        dst.save(output_path, deflate=True)
        dst.close()

    return {"fields_filled": filled, "output": output_path}


def main():
    parser = argparse.ArgumentParser(description="Fill ACORD 37 Statement of No Loss")
    parser.add_argument("--input", required=True, help="JSON data file")
    parser.add_argument("--form", required=True, help="Blank ACORD 37 PDF")
    parser.add_argument("--output", required=True, help="Output PDF path")
    parser.add_argument("--no-ocr", action="store_true", help="Skip OCR text layer")
    args = parser.parse_args()

    with open(args.input) as f:
        data = json.load(f)

    result = fill_acord37(data, args.form, args.output, ocr=not args.no_ocr)
    print(f"Done: {result['fields_filled']} fields filled -> {result['output']}")


if __name__ == "__main__":
    main()
