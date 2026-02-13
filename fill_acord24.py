#!/usr/bin/env python3
"""
ACORD 24 (Certificate of Property Insurance) Filler
Uses PyMuPDF (fitz) to fill the standard ACORD 24 form.

Usage:
    python fill_acord24.py --input data.json --form acord-24-blank.pdf --output filled.pdf
"""

import fitz
import json
import argparse
import subprocess
import os


FIELD_MAP = {
    "Form_CompletionDate_A": "date",
    "Producer_FullName_A": "agency_name",
    "Producer_MailingAddress_LineOne_A": "agency_address_1",
    "Producer_MailingAddress_LineTwo_A": "agency_address_2",
    "Producer_MailingAddress_CityName_A": "agency_city",
    "Producer_MailingAddress_StateOrProvinceCode_A": "agency_state",
    "Producer_MailingAddress_PostalCode_A": "agency_zip",
    "Producer_ContactPerson_FullName_A": "contact_name",
    "Producer_ContactPerson_PhoneNumber_A": "phone",
    "Producer_FaxNumber_A": "fax",
    "Producer_ContactPerson_EmailAddress_A": "email",
    "NamedInsured_FullName_A": "insured_name",
    "NamedInsured_MailingAddress_LineOne_A": "insured_address_1",
    "NamedInsured_MailingAddress_LineTwo_A": "insured_address_2",
    "NamedInsured_MailingAddress_CityName_A": "insured_city",
    "NamedInsured_MailingAddress_StateOrProvinceCode_A": "insured_state",
    "NamedInsured_MailingAddress_PostalCode_A": "insured_zip",
    "Insurer_FullName_A": "insurer_a", "Insurer_NAICCode_A": "naic_a",
    "Insurer_FullName_B": "insurer_b", "Insurer_NAICCode_B": "naic_b",
    "Property_InsurerLetterCode_A": "prop_insurer_letter",
    "Policy_Property_PolicyNumberIdentifier_A": "prop_policy_number",
    "Policy_Property_EffectiveDate_A": "prop_eff_date",
    "Policy_Property_ExpirationDate_A": "prop_exp_date",
    "CommercialProperty_Premises_DeductibleAmount_A": "prop_deductible",
    "Property_Building_LimitAmount_A": "prop_building_limit",
    "Property_PersonalProperty_LimitAmount_A": "prop_bpp_limit",
    "CommercialPropertyCoverage_BusinessIncome_LimitAmount_A": "prop_bi_limit",
    "CommercialPropertyCoverage_ExtraExpense_LimitAmount_A": "prop_ee_limit",
    "CommercialPropertyCoverage_RentalValue_LimitAmount_A": "prop_rental_limit",
    "CertificateOfLiabilityInsurance_ACORDForm_RemarkText_A": "location_description",
    "CertificateOfLiabilityInsurance_ACORDForm_RemarkText_B": "remarks",
    "CertificateHolder_FullName_A": "holder_name",
    "CertificateHolder_MailingAddress_LineOne_A": "holder_address_1",
    "CertificateHolder_MailingAddress_LineTwo_A": "holder_address_2",
    "CertificateHolder_MailingAddress_CityName_A": "holder_city",
    "CertificateHolder_MailingAddress_StateOrProvinceCode_A": "holder_state",
    "CertificateHolder_MailingAddress_PostalCode_A": "holder_zip",
}

CHECKBOX_MAP = {
    "Policy_PolicyType_PropertyIndicator_A": "type_property",
    "Policy_PolicyType_BasicIndicator_A": "cause_basic",
    "Policy_PolicyType_BroadIndicator_A": "cause_broad",
    "Policy_PolicyType_SpecialIndicator_A": "cause_special",
    "CommercialPropertyCoverage_EarthquakeOption_IncludedIndicator_A": "cause_earthquake",
    "Policy_PolicyType_WindIndicator_A": "cause_wind",
    "CommercialPropertyCoverage_Flood_YesIndicator_A": "cause_flood",
    "Property_Building_CoverageIndicator_A": "cov_building",
    "Property_PersonalProperty_CoverageIndicator_A": "cov_bpp",
    "CommercialPropertyCoverage_BusinessIncomeOption_IncludedIndicator_A": "cov_bi",
    "CommercialPropertyCoverage_ExtraExpenseOption_IncludedIndicator_A": "cov_ee",
    "CommercialPropertyCoverage_RentalValueOption_IncludedIndicator_A": "cov_rental",
}


def fill_acord24(data: dict, form_path: str, output_path: str,
                  signature_path: str = None, ocr: bool = True):
    doc = fitz.open(form_path)
    filled_t = filled_c = 0

    for widget in doc[0].widgets():
        fname = widget.field_name
        if fname in FIELD_MAP:
            key = FIELD_MAP[fname]
            value = data.get(key, "")
            if value:
                widget.field_value = str(value)
                widget.update()
                filled_t += 1
        elif fname in CHECKBOX_MAP:
            key = CHECKBOX_MAP[fname]
            if data.get(key):
                widget.field_value = True
                widget.update()
                filled_c += 1

    pix = doc[0].get_pixmap(dpi=200)
    dst = fitz.open()
    page = dst.new_page(width=doc[0].rect.width, height=doc[0].rect.height)
    page.insert_image(doc[0].rect, pixmap=pix)
    doc.close()

    if signature_path and os.path.exists(signature_path):
        from PIL import Image
        img = Image.open(signature_path)
        aspect = img.size[0] / img.size[1]
        sig_h = 22
        sig_w = int(sig_h * aspect)
        sig_x = 310 + (280 - sig_w) // 2
        sig_rect = fitz.Rect(sig_x, 721, sig_x + sig_w, 721 + sig_h)
        page.insert_image(sig_rect, filename=signature_path)

    if ocr:
        tmp = output_path + ".tmp.pdf"
        dst.save(tmp, deflate=True)
        dst.close()
        try:
            subprocess.run(["ocrmypdf", "--skip-text", "--optimize", "1", tmp, output_path],
                          capture_output=True, timeout=60)
            os.remove(tmp)
        except (FileNotFoundError, subprocess.TimeoutExpired):
            os.rename(tmp, output_path)
    else:
        dst.save(output_path, deflate=True)
        dst.close()

    return {"text_fields": filled_t, "checkboxes": filled_c, "output": output_path}


def main():
    parser = argparse.ArgumentParser(description="Fill ACORD 24 Certificate of Property Insurance")
    parser.add_argument("--input", required=True, help="JSON data file")
    parser.add_argument("--form", required=True, help="Blank ACORD 24 PDF")
    parser.add_argument("--output", required=True, help="Output PDF path")
    parser.add_argument("--signature", help="Path to signature image")
    parser.add_argument("--no-ocr", action="store_true", help="Skip OCR text layer")
    args = parser.parse_args()

    with open(args.input) as f:
        data = json.load(f)

    result = fill_acord24(data, args.form, args.output,
                           signature_path=args.signature, ocr=not args.no_ocr)
    print(f"Done: {result['text_fields']} text + {result['checkboxes']} checkboxes -> {result['output']}")


if __name__ == "__main__":
    main()
