#!/usr/bin/env python3
"""
ACORD 25 (Certificate of Liability Insurance) Filler
Uses PyMuPDF (fitz) to fill the standard ACORD 25 (2016/03) form.

Usage:
    python fill_acord25.py --input data.json --form acord-25-blank.pdf --output filled.pdf

Input JSON: see example_acord25.json
"""

import fitz
import json
import argparse
import subprocess
import os

P = "F[0].P1[0]."

FIELD_MAP = {
    # Header
    f"{P}Form_CompletionDate_A[0]": "date",
    # Producer
    f"{P}Producer_FullName_A[0]": "agency_name",
    f"{P}Producer_MailingAddress_LineOne_A[0]": "agency_address_1",
    f"{P}Producer_MailingAddress_LineTwo_A[0]": "agency_address_2",
    f"{P}Producer_MailingAddress_CityName_A[0]": "agency_city",
    f"{P}Producer_MailingAddress_StateOrProvinceCode_A[0]": "agency_state",
    f"{P}Producer_MailingAddress_PostalCode_A[0]": "agency_zip",
    f"{P}Producer_ContactPerson_FullName_A[0]": "contact_name",
    f"{P}Producer_ContactPerson_PhoneNumber_A[0]": "phone",
    f"{P}Producer_FaxNumber_A[0]": "fax",
    f"{P}Producer_ContactPerson_EmailAddress_A[0]": "email",
    # Insured
    f"{P}NamedInsured_FullName_A[0]": "insured_name",
    f"{P}NamedInsured_MailingAddress_LineOne_A[0]": "insured_address_1",
    f"{P}NamedInsured_MailingAddress_LineTwo_A[0]": "insured_address_2",
    f"{P}NamedInsured_MailingAddress_CityName_A[0]": "insured_city",
    f"{P}NamedInsured_MailingAddress_StateOrProvinceCode_A[0]": "insured_state",
    f"{P}NamedInsured_MailingAddress_PostalCode_A[0]": "insured_zip",
    # Insurers
    f"{P}Insurer_FullName_A[0]": "insurer_a", f"{P}Insurer_NAICCode_A[0]": "naic_a",
    f"{P}Insurer_FullName_B[0]": "insurer_b", f"{P}Insurer_NAICCode_B[0]": "naic_b",
    f"{P}Insurer_FullName_C[0]": "insurer_c", f"{P}Insurer_NAICCode_C[0]": "naic_c",
    # GL
    f"{P}GeneralLiability_InsurerLetterCode_A[0]": "gl_insurer_letter",
    f"{P}Policy_GeneralLiability_PolicyNumberIdentifier_A[0]": "gl_policy_number",
    f"{P}Policy_GeneralLiability_EffectiveDate_A[0]": "gl_eff_date",
    f"{P}Policy_GeneralLiability_ExpirationDate_A[0]": "gl_exp_date",
    f"{P}GeneralLiability_EachOccurrence_LimitAmount_A[0]": "gl_each_occurrence",
    f"{P}GeneralLiability_FireDamageRentedPremises_EachOccurrenceLimitAmount_A[0]": "gl_fire_damage",
    f"{P}GeneralLiability_MedicalExpense_EachPersonLimitAmount_A[0]": "gl_med_exp",
    f"{P}GeneralLiability_PersonalAndAdvertisingInjury_LimitAmount_A[0]": "gl_personal_adv_injury",
    f"{P}GeneralLiability_GeneralAggregate_LimitAmount_A[0]": "gl_general_agg",
    f"{P}GeneralLiability_ProductsAndCompletedOperations_AggregateLimitAmount_A[0]": "gl_products_agg",
    f"{P}GeneralLiability_OtherCoverageLimitDescription_A[0]": "gl_other_desc",
    f"{P}GeneralLiability_OtherCoverageLimitAmount_A[0]": "gl_other_limit",
    # Auto
    f"{P}Vehicle_InsurerLetterCode_A[0]": "auto_insurer_letter",
    f"{P}Policy_AutomobileLiability_PolicyNumberIdentifier_A[0]": "auto_policy_number",
    f"{P}Policy_AutomobileLiability_EffectiveDate_A[0]": "auto_eff_date",
    f"{P}Policy_AutomobileLiability_ExpirationDate_A[0]": "auto_exp_date",
    f"{P}Vehicle_CombinedSingleLimit_EachAccidentAmount_A[0]": "auto_combined_single",
    f"{P}Vehicle_BodilyInjury_PerPersonLimitAmount_A[0]": "auto_bi_person",
    f"{P}Vehicle_BodilyInjury_PerAccidentLimitAmount_A[0]": "auto_bi_accident",
    f"{P}Vehicle_PropertyDamage_PerAccidentLimitAmount_A[0]": "auto_pd",
    # Umbrella/Excess
    f"{P}ExcessUmbrella_InsurerLetterCode_A[0]": "umb_insurer_letter",
    f"{P}Policy_ExcessLiability_PolicyNumberIdentifier_A[0]": "umb_policy_number",
    f"{P}Policy_ExcessLiability_EffectiveDate_A[0]": "umb_eff_date",
    f"{P}Policy_ExcessLiability_ExpirationDate_A[0]": "umb_exp_date",
    f"{P}ExcessUmbrella_Umbrella_EachOccurrenceAmount_A[0]": "umb_each_occurrence",
    f"{P}ExcessUmbrella_Umbrella_AggregateAmount_A[0]": "umb_aggregate",
    f"{P}ExcessUmbrella_Umbrella_DeductibleOrRetentionAmount_A[0]": "umb_ded_retention",
    # WC
    f"{P}WorkersCompensationEmployersLiability_InsurerLetterCode_A[0]": "wc_insurer_letter",
    f"{P}Policy_WorkersCompensationAndEmployersLiability_PolicyNumberIdentifier_A[0]": "wc_policy_number",
    f"{P}Policy_WorkersCompensationAndEmployersLiability_EffectiveDate_A[0]": "wc_eff_date",
    f"{P}Policy_WorkersCompensationAndEmployersLiability_ExpirationDate_A[0]": "wc_exp_date",
    f"{P}WorkersCompensationEmployersLiability_EmployersLiability_EachAccidentLimitAmount_A[0]": "wc_each_accident",
    f"{P}WorkersCompensationEmployersLiability_EmployersLiability_DiseaseEachEmployeeLimitAmount_A[0]": "wc_disease_employee",
    f"{P}WorkersCompensationEmployersLiability_EmployersLiability_DiseasePolicyLimitAmount_A[0]": "wc_disease_policy",
    # Description / Remarks
    f"{P}CertificateOfLiabilityInsurance_ACORDForm_RemarkText_A[0]": "description",
    # Certificate Holder
    f"{P}CertificateHolder_FullName_A[0]": "holder_name",
    f"{P}CertificateHolder_MailingAddress_LineOne_A[0]": "holder_address_1",
    f"{P}CertificateHolder_MailingAddress_LineTwo_A[0]": "holder_address_2",
    f"{P}CertificateHolder_MailingAddress_CityName_A[0]": "holder_city",
    f"{P}CertificateHolder_MailingAddress_StateOrProvinceCode_A[0]": "holder_state",
    f"{P}CertificateHolder_MailingAddress_PostalCode_A[0]": "holder_zip",
}

CHECKBOX_MAP = {
    f"{P}GeneralLiability_CoverageIndicator_A[0]": "gl_enabled",
    f"{P}GeneralLiability_OccurrenceIndicator_A[0]": "gl_occurrence",
    f"{P}GeneralLiability_ClaimsMadeIndicator_A[0]": "gl_claims_made",
    f"{P}GeneralLiability_GeneralAggregate_LimitAppliesPerPolicyIndicator_A[0]": "gl_agg_per_policy",
    f"{P}GeneralLiability_GeneralAggregate_LimitAppliesPerProjectIndicator_A[0]": "gl_agg_per_project",
    f"{P}GeneralLiability_GeneralAggregate_LimitAppliesPerLocationIndicator_A[0]": "gl_agg_per_location",
    f"{P}Vehicle_AnyAutoIndicator_A[0]": "auto_any",
    f"{P}Vehicle_AllOwnedAutosIndicator_A[0]": "auto_owned",
    f"{P}Vehicle_HiredAutosIndicator_A[0]": "auto_hired",
    f"{P}Vehicle_ScheduledAutosIndicator_A[0]": "auto_scheduled",
    f"{P}Vehicle_NonOwnedAutosIndicator_A[0]": "auto_non_owned",
    f"{P}Policy_PolicyType_UmbrellaIndicator_A[0]": "umb_umbrella",
    f"{P}Policy_PolicyType_ExcessIndicator_A[0]": "umb_excess",
    f"{P}ExcessUmbrella_OccurrenceIndicator_A[0]": "umb_occurrence",
    f"{P}ExcessUmbrella_ClaimsMadeIndicator_A[0]": "umb_claims_made",
    f"{P}ExcessUmbrella_DeductibleIndicator_A[0]": "umb_deductible",
    f"{P}ExcessUmbrella_RetentionIndicator_A[0]": "umb_retention",
    f"{P}WorkersCompensationEmployersLiability_WorkersCompensationStatutoryLimitIndicator_A[0]": "wc_statutory",
}


def fill_acord25(data: dict, form_path: str, output_path: str, 
                  signature_path: str = None, ocr: bool = True):
    """Fill an ACORD 25 Certificate of Liability Insurance.
    
    Args:
        data: Dictionary with form field values
        form_path: Path to blank ACORD 25 PDF
        output_path: Path for output PDF
        signature_path: Optional path to signature image
        ocr: Whether to add OCR text layer
    
    Returns:
        dict with fill stats
    """
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

    # Flatten
    pix = doc[0].get_pixmap(dpi=200)
    dst = fitz.open()
    page = dst.new_page(width=doc[0].rect.width, height=doc[0].rect.height)
    page.insert_image(doc[0].rect, pixmap=pix)
    doc.close()

    # Signature
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
    parser = argparse.ArgumentParser(description="Fill ACORD 25 Certificate of Liability Insurance")
    parser.add_argument("--input", required=True, help="JSON data file")
    parser.add_argument("--form", required=True, help="Blank ACORD 25 PDF")
    parser.add_argument("--output", required=True, help="Output PDF path")
    parser.add_argument("--signature", help="Path to signature image")
    parser.add_argument("--no-ocr", action="store_true", help="Skip OCR text layer")
    args = parser.parse_args()

    with open(args.input) as f:
        data = json.load(f)

    result = fill_acord25(data, args.form, args.output, 
                           signature_path=args.signature, ocr=not args.no_ocr)
    print(f"Done: {result['text_fields']} text + {result['checkboxes']} checkboxes -> {result['output']}")


if __name__ == "__main__":
    main()
