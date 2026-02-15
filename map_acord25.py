#!/usr/bin/env python3
"""
ACORD 25 Field Mapping — Maps structured policy data to ACORD 25 PDF field names.

Supports multiple insurers (A-E) with per-coverage-line carrier, policy number, and dates.
Use with fill_acord.py to generate filled ACORD 25 certificates.

Usage:
    from map_acord25 import map_to_acord25
    fields = map_to_acord25(policy_data, cert_holder, agency)
    # Then pass `fields` to fill_acord_form()
"""

from datetime import datetime


def map_to_acord25(policy_data: dict, cert_holder: dict, agency: dict) -> dict:
    """Map policy data to ACORD 25 fields. Supports multiple insurers/policies per coverage line."""
    fields = {}
    today = datetime.now().strftime("%m/%d/%Y")
    ins = policy_data.get("insured", {})
    pol = policy_data.get("policy", {})  # legacy single-policy fallback
    cov = policy_data.get("coverages", {})
    gl = cov.get("gl", {})
    auto = cov.get("auto", {})
    umb = cov.get("umbrella", {})
    wc = cov.get("workers_comp", {})
    p = "F[0].P1[0]."
    
    # Insurers table: supports up to 5 (A-E)
    # New format: policy_data.insurers = [{letter: "A", carrier: "...", naic: "..."}, ...]
    # Legacy format: policy_data.policy.carrier goes into slot A
    insurers = policy_data.get("insurers", [])
    if not insurers and pol.get("carrier"):
        insurers = [{"letter": "A", "carrier": pol["carrier"], "naic": pol.get("naic", "")}]
    
    for insurer in insurers[:5]:
        letter = insurer.get("letter", "A")
        idx = ord(letter) - ord("A")  # A=0, B=1, etc.
        fields[f"{p}Insurer_FullName_{letter}[0]"] = insurer.get("carrier", "")
        fields[f"{p}Insurer_NAICCode_{letter}[0]"] = insurer.get("naic", "")
    
    # Also fill the legacy single-insurer field for backwards compat
    if insurers:
        fields[f"{p}Insurer_FullName_A[0]"] = insurers[0].get("carrier", "")
        fields[f"{p}Insurer_NAICCode_A[0]"] = insurers[0].get("naic", "")
    
    fields[f"{p}Form_CompletionDate_A[0]"] = today
    
    # Producer
    fields[f"{p}Producer_FullName_A[0]"] = agency.get("name", "")
    addr_parts = [agency.get("address_line1", agency.get("address", ""))]
    if agency.get("address_line2"):
        addr_parts.append(agency["address_line2"])
    fields[f"{p}Producer_MailingAddress_LineOne_A[0]"] = "\n".join(addr_parts)
    fields[f"{p}Producer_MailingAddress_CityName_A[0]"] = agency.get("city", "")
    fields[f"{p}Producer_MailingAddress_StateOrProvinceCode_A[0]"] = agency.get("state", "")
    fields[f"{p}Producer_MailingAddress_PostalCode_A[0]"] = agency.get("zip", "")
    fields[f"{p}Producer_ContactPerson_FullName_A[0]"] = agency.get("contact", "")
    fields[f"{p}Producer_ContactPerson_PhoneNumber_A[0]"] = agency.get("phone", "")
    fields[f"{p}Producer_ContactPerson_EmailAddress_A[0]"] = agency.get("email", "")
    
    # Insured
    fields[f"{p}NamedInsured_FullName_A[0]"] = ins.get("name", "")
    addr = ins.get("address_line1", "")
    if ins.get("address_line2"):
        addr += "\n" + ins["address_line2"]
    fields[f"{p}NamedInsured_MailingAddress_LineOne_A[0]"] = addr
    fields[f"{p}NamedInsured_MailingAddress_CityName_A[0]"] = ins.get("city", "")
    fields[f"{p}NamedInsured_MailingAddress_StateOrProvinceCode_A[0]"] = ins.get("state", "")
    fields[f"{p}NamedInsured_MailingAddress_PostalCode_A[0]"] = ins.get("zip", "")
    
    # Helper: get per-line dates, falling back to legacy single policy
    def line_dates(line_data):
        eff = line_data.get("effective_date", pol.get("effective_date", ""))
        exp = line_data.get("expiration_date", pol.get("expiration_date", ""))
        return eff, exp
    
    # GL
    if gl.get("has"):
        letter = gl.get("insurer_letter", "A")
        eff, exp = line_dates(gl)
        fields[f"{p}GeneralLiability_CoverageIndicator_A[0]"] = "Yes"
        if gl.get("occurrence"): fields[f"{p}GeneralLiability_OccurrenceIndicator_A[0]"] = "Yes"
        if gl.get("claims_made"): fields[f"{p}GeneralLiability_ClaimsMadeIndicator_A[0]"] = "Yes"
        fields[f"{p}GeneralLiability_InsurerLetterCode_A[0]"] = letter
        fields[f"{p}GeneralLiability_PolicyNumberIdentifier_A[0]"] = gl.get("policy_number", pol.get("number", ""))
        fields[f"{p}GeneralLiability_PolicyEffectiveDate_A[0]"] = eff
        fields[f"{p}GeneralLiability_PolicyExpirationDate_A[0]"] = exp
        fields[f"{p}GeneralLiability_EachOccurrence_LimitAmount_A[0]"] = gl.get("occurrence_limit", "")
        fields[f"{p}GeneralLiability_GeneralAggregate_LimitAmount_A[0]"] = gl.get("aggregate_limit", "")
        fields[f"{p}GeneralLiability_FireDamageRentedPremises_EachOccurrenceLimitAmount_A[0]"] = gl.get("fire_damage_limit", "")
        fields[f"{p}GeneralLiability_MedicalExpense_AnyOnePersonLimitAmount_A[0]"] = gl.get("med_exp_limit", "")
        fields[f"{p}GeneralLiability_PersonalAndAdvertisingInjury_LimitAmount_A[0]"] = gl.get("personal_adv_limit", "")
        fields[f"{p}GeneralLiability_ProductsCompletedOperationsAggregate_LimitAmount_A[0]"] = gl.get("products_completed_limit", "")
    
    # Auto
    if auto.get("has"):
        letter = auto.get("insurer_letter", "B")
        eff, exp = line_dates(auto)
        fields[f"{p}AutomobileLiability_InsurerLetterCode_A[0]"] = letter
        fields[f"{p}AutomobileLiability_PolicyNumberIdentifier_A[0]"] = auto.get("policy_number", "")
        fields[f"{p}AutomobileLiability_PolicyEffectiveDate_A[0]"] = eff
        fields[f"{p}AutomobileLiability_PolicyExpirationDate_A[0]"] = exp
        fields[f"{p}AutomobileLiability_CombinedSingleLimit_EachAccidentAmount_A[0]"] = auto.get("combined_single_limit", "")
        if auto.get("any_auto"): fields[f"{p}AutomobileLiability_AnyAutoIndicator_A[0]"] = "Yes"
        if auto.get("hired"): fields[f"{p}AutomobileLiability_HiredAutosOnlyIndicator_A[0]"] = "Yes"
        if auto.get("non_owned"): fields[f"{p}AutomobileLiability_NonOwnedAutosOnlyIndicator_A[0]"] = "Yes"
    
    # Umbrella
    if umb.get("has"):
        letter = umb.get("insurer_letter", "C")
        eff, exp = line_dates(umb)
        fields[f"{p}ExcessUmbrella_InsurerLetterCode_A[0]"] = letter
        fields[f"{p}ExcessUmbrella_PolicyNumberIdentifier_A[0]"] = umb.get("policy_number", "")
        fields[f"{p}ExcessUmbrella_PolicyEffectiveDate_A[0]"] = eff
        fields[f"{p}ExcessUmbrella_PolicyExpirationDate_A[0]"] = exp
        fields[f"{p}ExcessUmbrella_Umbrella_EachOccurrenceAmount_A[0]"] = umb.get("each_occurrence", "")
        fields[f"{p}ExcessUmbrella_Umbrella_AggregateAmount_A[0]"] = umb.get("aggregate", "")
    
    # WC
    if wc.get("has"):
        letter = wc.get("insurer_letter", "D")
        eff, exp = line_dates(wc)
        fields[f"{p}WorkersCompensation_InsurerLetterCode_A[0]"] = letter
        fields[f"{p}WorkersCompensation_PolicyNumberIdentifier_A[0]"] = wc.get("policy_number", "")
        fields[f"{p}WorkersCompensation_PolicyEffectiveDate_A[0]"] = eff
        fields[f"{p}WorkersCompensation_PolicyExpirationDate_A[0]"] = exp
        if wc.get("statutory"): fields[f"{p}WorkersCompensation_StatutoryLimitsIndicator_A[0]"] = "Yes"
        fields[f"{p}WorkersCompensation_EachAccident_LimitAmount_A[0]"] = wc.get("el_each_accident", "")
        fields[f"{p}WorkersCompensation_DiseasePolicyLimit_LimitAmount_A[0]"] = wc.get("el_disease_policy", "")
        fields[f"{p}WorkersCompensation_DiseaseEachEmployee_LimitAmount_A[0]"] = wc.get("el_disease_each", "")
    
    # Certificate Holder
    ch = cert_holder
    fields[f"{p}CertificateHolder_FullName_A[0]"] = ch.get("name", "")
    fields[f"{p}CertificateHolder_MailingAddress_LineOne_A[0]"] = ch.get("address_line1", "")
    fields[f"{p}CertificateHolder_MailingAddress_LineTwo_A[0]"] = ch.get("address_line2", "")
    fields[f"{p}CertificateHolder_MailingAddress_CityName_A[0]"] = ch.get("city", "")
    fields[f"{p}CertificateHolder_MailingAddress_StateOrProvinceCode_A[0]"] = ch.get("state", "")
    fields[f"{p}CertificateHolder_MailingAddress_PostalCode_A[0]"] = ch.get("zip", "")
    
    # Description
    desc_parts = []
    if ch.get("additional_insured"):
        desc_parts.append(f"{ch['name']} is included as Additional Insured as required by written contract.")
    if ch.get("waiver_of_subrogation"):
        desc_parts.append("Waiver of Subrogation applies in favor of the Certificate Holder as required by written contract.")
    if ch.get("primary_noncontributory"):
        desc_parts.append("Coverage is Primary and Non-Contributory as required by written contract.")
    if ch.get("additional_description"):
        desc_parts.append(ch["additional_description"])
    if desc_parts:
        fields[f"{p}CertificateOfLiabilityInsurance_ACORDForm_RemarkText_A[0]"] = "\n".join(desc_parts)
    
    if ch.get("additional_insured"):
        if gl.get("has"): fields[f"{p}CertificateOfInsurance_GeneralLiability_AdditionalInsuredCode_A[0]"] = "Y"
        if auto.get("has"): fields[f"{p}CertificateOfInsurance_AutomobileLiability_AdditionalInsuredCode_A[0]"] = "Y"
    
    return fields


