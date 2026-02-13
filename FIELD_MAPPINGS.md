# ACORD 125/140 Field Mappings

Complete reference of all 924 fillable field names in the ACORD 125 (Commercial Insurance Application) and ACORD 140 (Property Section). Field names are extracted from the standard fillable PDF via PyMuPDF widgets.

> **Note:** Field names may vary slightly between ACORD form editions. These mappings are based on the current standard fillable PDF.

---

## Page 1 — Agency, Carrier & Policy Info

### Agency / Producer
| Field Name | Type | Description |
|---|---|---|
| `ACORD_AgencyName` | Text | Agency name and address (multi-line) |
| `ACORD_ProducerContact` | Text | Producer contact name |
| `ACORD_ProducerPhoneNumber` | Text | Producer phone |
| `ACORD_ProducerFaxNumber` | Text | Producer fax |
| `ACORD_ProducerEmailAddress` | Text | Producer email |
| `ACORD_ProducerCode` | Text | Producer code |
| `ACORD_ProducerSubCode` | Text | Producer sub-code |
| `ACORD_ProgramCode` | Text | Program code |
| `ACORD_ProgramName` | Text | Program name |

### Carrier
| Field Name | Type | Description |
|---|---|---|
| `ACORD_CarrierName` | Text | Insurance carrier name |
| `ACORD_NAICCode` | Text | NAIC code |
| `ACORD_Underwriter` | Text | Underwriter name |
| `ACORD_UnderwriterOffice` | Text | Underwriter office |

### Policy
| Field Name | Type | Description |
|---|---|---|
| `ACORD_PolicyNumber` | Text | Policy number |
| `ACORD_Policy_EffectiveDate` | Text | Policy effective date (MM/DD/YYYY) |
| `ACORD_Policy_ExpirationDate` | Text | Policy expiration date |
| `ACORD_Policy_PolicyPremium` | Text | Total policy premium |
| `ACORD_Policy_MinimumPremium` | Text | Minimum premium |
| `ACORD_Policy_DepositAmount` | Text | Deposit amount |
| `ACORD_Policy_PaymentPlan` | Text | Payment plan |
| `ACORD_Policy_PaymentMethod` | Text | Payment method |
| `ACORD_Policy_Audit` | Text | Audit |
| `ACORD_Policy_AgencyPlan` | CheckBox | Agency bill |
| `ACORD_Policy_DirectPlan` | CheckBox | Direct bill |
| `ACORD_CurrentDate` | Text | Date form completed |

### Transaction Type (check one)
| Field Name | Type | Description |
|---|---|---|
| `ACORD_Transaction_Quote` | CheckBox | Quote |
| `ACORD_Transaction_Bound` | CheckBox | Bound |
| `ACORD_Transaction_Renew` | CheckBox | Renewal |
| `ACORD_Transaction_Cancel` | CheckBox | Cancellation |
| `ACORD_Transaction_Change` | CheckBox | Endorsement/change |
| `ACORD_Transaction_IssuePolicy` | CheckBox | Issue policy |
| `ACORD_Transaction_Date` | Text | Transaction date |
| `ACORD_Transaction_Time` | Text | Transaction time |
| `ACORD_Transaction_Time_AM` | CheckBox | AM |
| `ACORD_Transaction_Time_PM` | CheckBox | PM |

### LOB Checkboxes
| Field Name | Type | Description |
|---|---|---|
| `ACORD_LOB_BusinessAuto` | CheckBox | Business Auto line |
| `ACORD_LOB_BusinessAuto_Premium` | Text | Business Auto premium |

### Insured (up to 3 named insureds)
| Field Name | Type | Description |
|---|---|---|
| `ACORD_Policy_Insured1_Name` | Text | Named insured #1 |
| `ACORD_Policy_Insured1_MailingAddress` | Text | Mailing address |
| `ACORD_Policy_Insured1_PhoneNumber` | Text | Phone |
| `ACORD_Policy_Insured1_SIC` | Text | SIC code |
| `ACORD_Policy_Insured1_NAICS` | Text | NAICS code |
| `ACORD_Policy_Insured1_GLCode` | Text | GL class code |
| `ACORD_Policy_Insured1_FEINSSN` | Text | FEIN/SSN |
| `ACORD_Policy_Insured1_Website` | Text | Website |

#### Entity Type Checkboxes (Insured 1)
| Field Name | Type |
|---|---|
| `ACORD_Policy_Insured1_Type_LLC` | CheckBox |
| `ACORD_Policy_Insured1_Type_Corporation` | CheckBox |
| `ACORD_Policy_Insured1_Type_SCorp` | CheckBox |
| `ACORD_Policy_Insured1_Type_Partnership` | CheckBox |
| `ACORD_Policy_Insured1_Type_Individual` | CheckBox |
| `ACORD_Policy_Insured1_Type_JointVenture` | CheckBox |
| `ACORD_Policy_Insured1_Type_Trust` | CheckBox |
| `ACORD_Policy_Insured1_Type_NotForProfit` | CheckBox |
| `ACORD_Policy_Insured1_Type_NumberofMembers` | Text |

> Insured 2 and 3 follow the same pattern: `ACORD_Policy_Insured2_*`, `ACORD_Policy_Insured3_*`

---

## Page 2 — Locations & Nature of Business

### Locations (up to 4)
Each location uses the pattern `ACORD_Location{N}_*` where N = 1–4.

| Field Name Pattern | Type | Description |
|---|---|---|
| `ACORD_Location{N}_LocationNumber` | Text | Location/premises number |
| `ACORD_Location{N}_BuildingNumber` | Text | Building number |
| `ACORD_Location{N}_Street` | Text | Street address |
| `ACORD_Location{N}_City` | Text | City |
| `ACORD_Location{N}_State` | Text | State |
| `ACORD_Location{N}_ZIP` | Text | ZIP code |
| `ACORD_Location{N}_County` | Text | County |
| `ACORD_Location{N}_Description` | Text | Building/occupancy description |
| `ACORD_Location{N}_BuildingArea` | Text | Total building area (sqft) |
| `ACORD_Location{N}_OccupiedArea` | Text | Area occupied by insured |
| `ACORD_Location{N}_PublicArea` | Text | Public area |
| `ACORD_Location{N}_LeasedToOthers` | Text | Area leased to others |
| `ACORD_Location{N}_AnnualRevenue` | Text | Annual revenue at location |
| `ACORD_Location{N}_Employees_FullTime` | Text | Full-time employee count |
| `ACORD_Location{N}_Employees_PartTime` | Text | Part-time employee count |
| `ACORD_Location{N}_Interest_Owner` | CheckBox | Owner interest |
| `ACORD_Location{N}_Interest_Tenant` | CheckBox | Tenant interest |
| `ACORD_Location{N}_CityLimits_Inside` | CheckBox | Inside city limits |
| `ACORD_Location{N}_CityLimits_Outside` | CheckBox | Outside city limits |

### Nature of Business
| Field Name | Type | Description |
|---|---|---|
| `ACORD_NatureOfBusiness_Description` | Text | Description of operations |
| `ACORD_NatureOfBusiness_StartDate` | Text | Business start date |
| `ACORD_NatureOfBusiness_Retail` | CheckBox | Retail |
| `ACORD_NatureOfBusiness_Wholesale` | CheckBox | Wholesale |
| `ACORD_NatureOfBusiness_Manufacturing` | CheckBox | Manufacturing |
| `ACORD_NatureOfBusiness_Service` | CheckBox | Service |
| `ACORD_NatureOfBusiness_Contractor` | CheckBox | Contractor |
| `ACORD_NatureOfBusiness_Office` | CheckBox | Office |
| `ACORD_NatureOfBusiness_Restaurant` | CheckBox | Restaurant |
| `ACORD_NatureOfBusiness_Apartments` | CheckBox | Apartments |
| `ACORD_NatureOfBusiness_Condominiums` | CheckBox | Condominiums |
| `ACORD_NatureOfBusiness_Institutional` | CheckBox | Institutional |
| `ACORD_NatureOfBusiness_RetailPercentage` | Text | Retail % |
| `ACORD_NatureOfBusiness_InstallationPercentage` | Text | Installation % |
| `ACORD_NatureOfBusiness_OffPremisesInstallation` | Text | Off-premises installation |

### Contacts
| Field Name Pattern | Type | Description |
|---|---|---|
| `ACORD_Contact{N}_Name` | Text | Contact name (N=1,2) |
| `ACORD_Contact{N}_Type` | Text | Contact type |
| `ACORD_Contact{N}_PrimaryPhoneNumber` | Text | Primary phone |
| `ACORD_Contact{N}_PrimaryEmailAddress` | Text | Primary email |
| `ACORD_Contact{N}_PrimaryBusinessPhone` | CheckBox | Business phone |
| `ACORD_Contact{N}_PrimaryCellPhone` | CheckBox | Cell phone |
| `ACORD_Contact{N}_PrimaryHomePhone` | CheckBox | Home phone |

### Additional Insured / Interest (Page 2)
| Field Name | Type |
|---|---|
| `ACORD_125_Interest_1_NameAddress` | Text |
| `ACORD_125_Interest_1_Owner` | CheckBox |
| `ACORD_125_Interest_1_Lienholder` | CheckBox |
| `ACORD_125_Interest_1_LossPayee` | CheckBox |
| `ACORD_125_Interest_1_AdditionalInsured` | CheckBox |
| `ACORD_125_Interest_1_Certificate` | CheckBox |
| `ACORD_125_Interest_1_LienAmount` | Text |
| `ACORD_125_Interest_1_ReferenceNumber` | Text |
| `ACORD_125_Interest_1_ReasonForInterest` | Text |
| `ACORD_125_Interest_1_EmailAddress` | Text |
| `ACORD_125_Interest_1_PhoneNumber` | Text |
| `ACORD_125_Interest_1_FaxNumber` | Text |

---

## Page 3 — General Information & Prior Carrier

### General Information Y/N Questions

⚠️ **WORKAROUND:** These checkbox widgets do NOT accept text via the widget API. You must draw "Y" or "N" as text overlays at specific coordinates after flattening the PDF.

| Field Name | CheckBox Field | Y x-coord | N x-coord | y-coord | Description |
|---|---|---|---|---|---|
| Coverage Terminated | `ACORD_General_CoverageTerminated` | 498 | 524 | 164 | Has coverage been terminated? |
| Subsidiary | `ACORD_General_Subsidiary` | 498 | 524 | 179 | Is applicant a subsidiary? |
| Parent | `ACORD_General_Parent` | 498 | 524 | 194 | Is applicant a parent company? |
| Other Ventures | `ACORD_General_OtherVentures` | 498 | 524 | 232 | Other business ventures? |
| Exposure | `ACORD_General_Exposure` | 498 | 524 | 247 | Environmental exposure? |
| Foreign | `ACORD_General_Foreign` | 498 | 524 | 262 | Foreign operations? |
| Trust | `ACORD_General_Trust` | 498 | 524 | 277 | Held in trust? |
| Other Insurance | `ACORD_General_OtherInsurance` | 498 | 524 | 315 | Other insurance? |
| Possess Drones | `ACORD_General_PossessDrones` | 498 | 524 | 353 | Possess drones? |
| Hire Drones | `ACORD_General_HireDrones` | 498 | 524 | 368 | Hire drones? |
| Indicted/Convicted | `ACORD_General_IndictedOrConvicted` | 498 | 524 | 406 | Indicted or convicted? |
| Safety Violations | `ACORD_General_SafetyViolations` | 498 | 524 | 421 | Safety violations? |
| Financial Action | `ACORD_General_NegativeFinancialAction` | 498 | 524 | 459 | Negative financial action? |
| Judgement/Lien | `ACORD_General_JudgementLien` | 498 | 524 | 474 | Judgement or lien? |
| Safety Program | `ACORD_General_Safety` | 498 | 524 | 512 | Safety program? |
| Past Allegations | `ACORD_General_PastAllegations` | 498 | 524 | 550 | Past allegations? |

**Typical usage:** For most commercial property renewals, all answers are "N". Set `"general_info_all_no": true` in the config. Override individual questions via the `"general_info"` dict.

### General Info Sub-fields
When a Y/N answer is "Y", additional detail fields are available:

| Field Name | Type | Description |
|---|---|---|
| `ACORD_General_CoverageTerminated_NonPayment` | CheckBox | Terminated for non-payment |
| `ACORD_General_CoverageTerminated_NonRenewal` | CheckBox | Non-renewal |
| `ACORD_General_CoverageTerminated_Underwriting` | CheckBox | Underwriting |
| `ACORD_General_CoverageTerminated_AgentStopRepresenting` | CheckBox | Agent stopped representing |
| `ACORD_General_CoverageTerminated_ConditionCorrected` | CheckBox | Condition corrected |
| `ACORD_General_CoverageTerminated_ConditionCorrected_Description` | Text | Description |
| `ACORD_General_Subsidiary_Parent` | Text | Parent company name |
| `ACORD_General_Subsidiary_Relationship` | Text | Relationship |
| `ACORD_General_Subsidiary_OwnershipPercentage` | Text | Ownership % |
| `ACORD_General_Parent_SubsidaryName` | Text | Subsidiary name |
| `ACORD_General_Parent_Relationship` | Text | Relationship |
| `ACORD_General_Parent_OwnershipPercentage` | Text | Ownership % |
| `ACORD_General_OtherVentures_Description` | Text | Description |
| `ACORD_General_Exposure_Description` | Text | Exposure description |
| `ACORD_General_Trust_Name` | Text | Trust name |
| `ACORD_General_PossessDrones_Description` | Text | Drone details |
| `ACORD_General_HireDrones_Description` | Text | Hired drone details |
| `ACORD_General_IndictedOrConvicted_Description` | Text | Details |
| `ACORD_General_PastAllegations_Description` | Text | Details |
| `ACORD_General_Remarks` | Text | General remarks |

### Other Insurance (when Y)
| Field Name | Type |
|---|---|
| `ACORD_General_OtherInsurance_{N}_LOB` | Text (N=1-4) |
| `ACORD_General_OtherInsurance_{N}_PolicyNumber` | Text (N=1-4) |

### Safety Violations / Financial / Judgement Detail
Pattern: `ACORD_General_{Section}_{N}_Explanation`, `_OccurenceDate`, `_Resolution`, `_ResolutionDate` (N=1,2)

Sections: `SafetyViolations`, `NegativeFinancialAction`, `JudgementLien`

### Safety Program (when Y)
| Field Name | Type |
|---|---|
| `ACORD_General_Safety_SafetyManual` | CheckBox |
| `ACORD_General_Safety_SafetyPosition` | CheckBox |
| `ACORD_General_Safety_OSHA` | CheckBox |
| `ACORD_General_Safety_MonthlyMeetings` | CheckBox |
| `ACORD_General_Safety_Other` | CheckBox |
| `ACORD_General_Safety_Other_Text` | Text |

### Prior Carrier (up to 3 years)

⚠️ **WORKAROUND:** The field names say "Auto" but the columns are generic. For **Property** policies, the Property column data must be drawn manually at **x:355** after flattening. The "Auto" fields are the only widget fields available.

| Field Name | Type | Description |
|---|---|---|
| `ACORD_PriorCarrier_1_AutoCarrier` | Text | Prior carrier name (year 1) |
| `ACORD_PriorCarrier_1_AutoPolicyNumber` | Text | Prior policy number |
| `ACORD_PriorCarrier_1_AutoPremium` | Text | Prior premium |
| `ACORD_PriorCarrier_1_AutoEffectiveDate` | Text | Prior eff date |
| `ACORD_PriorCarrier_1_AutoExpirationDate` | Text | Prior exp date |
| `ACORD_PriorCarrier_1_AutoYear` | Text | Year |

> Rows 2 and 3: `ACORD_PriorCarrier_2_Auto*` (page 4), `ACORD_PriorCarrier_3_Auto*` (page 4)

---

## Page 4 — Loss History, Signatures & Remarks

### Loss History
| Field Name | Type | Description |
|---|---|---|
| `ACORD_LossHistory_None` | CheckBox | Check if no losses |
| `ACORD_LossHistory_NumberOfYears` | Text | Number of years shown |
| `ACORD_LossHistory_TotalLosses` | Text | Total losses |

#### Loss History Rows (up to 3)
Pattern: `ACORD_LossHistory_{N}_*` where N = 1–3

| Field Suffix | Type | Description |
|---|---|---|
| `_DateOfClaim` | Text | Date of claim |
| `_OccurenceDate` | Text | Date of occurrence |
| `_Description` | Text | Loss description |
| `_LOB` | Text | Line of business |
| `_AmountPaid` | Text | Amount paid |
| `_AmountReserved` | Text | Amount reserved |
| `_ClaimOpen` | Text | Claim open (Y/N) |
| `_Subrogation` | Text | Subrogation (Y/N) |

### Signatures
| Field Name | Type |
|---|---|
| `ACORD_Signatures_Applicant_Signature` | Text |
| `ACORD_Signatures_Applicant_Date` | Text |
| `ACORD_Signatures_Applicant_Initials` | Text |
| `ACORD_Signatures_Producer_Signature` | Text |
| `ACORD_Signatures_Producer_Name` | Text |
| `ACORD_Signatures_Producer_LicenseNumber` | Text |
| `ACORD_Signatures_Producer_NationalNumber` | Text |
| `ACORD_AgencyCustomerID` | Text |

---

## Pages 5–8 — General Liability (GL Section)

> Skip these pages for property-only policies using `--skip-gl`.

These pages contain GL classification, hazard codes, limits, and GL-specific questions. Key fields include:

- `GeneralLiability_*` — Limits, deductibles, hazard classifications
- `GeneralLiabilityLineOfBusiness_*` — GL-specific Y/N questions and explanations
- `Contractors_*` — Contractor-specific questions
- `ProductAndCompletedOperations_*` — Product liability fields
- `SwimmingPool_*`, `AthleticTeam_*` — Special exposure fields

See full field dump via `python acord_filler.py --form blank.pdf --list-fields` for all GL fields.

---

## Pages 9–10 — ACORD 140 Property Section

### Section Layout
- **Page 9 (Section A)** — Coverage rows A through E = **Location 1**
- **Page 10 (Section B)** — Coverage rows G through K = **Location 2**

Fields use suffix `_A` for Section A and `_B` for Section B.

### Header / Identification
| Field Name | Type | Description |
|---|---|---|
| `NamedInsured_FullName_A` | Text | Named insured |
| `Policy_PolicyNumberIdentifier_A` | Text | Policy number |
| `Policy_EffectiveDate_A` | Text | Effective date |
| `Insurer_FullName_A` / `Insurer_NAICCode_A` | Text | Carrier info |
| `Producer_FullName_A` | Text | Producer/agency name |
| `Form_CompletionDate_A` / `Form_EditionIdentifier_A` | Text | Form metadata |

### Premises / Building Info
| Field Pattern | Type | Description |
|---|---|---|
| `CommercialStructure_Location_ProducerIdentifier_{A/B}` | Text | Premises # |
| `CommercialStructure_Building_ProducerIdentifier_{A/B}` | Text | Building # |
| `CommercialStructure_PhysicalAddress_LineOne_{A/B}` | Text | Street address |
| `CommercialStructure_Building_SublocationDescription_{A/B}` | Text | Building description |

### Construction
| Field Pattern | Type | Description |
|---|---|---|
| `Construction_ConstructionCode_{A/B}` | Text | ISO construction code (Frame, JM, NC, MNC, MFR, FR) |
| `CommercialStructure_BuiltYear_{A/B}` | Text | Year built |
| `Construction_StoreyCount_{A/B}` | Text | Number of stories |
| `Construction_BasementCount_{A/B}` | Text | Number of basements (0 for TX Gulf Coast) |
| `Construction_BuildingArea_{A/B}` | Text | Building area (sqft) |
| `Construction_RoofMaterialCode_{A/B}` | Text | Roof material |
| `Construction_OpenSidesCount_{A/B}` | Text | Open sides count |
| `Construction_BuildingCodeEffectivenessGradeCode_{A/B}` | Text | BCEG code |

### ISO Construction Code Reference
| Code | Description | Typical Example |
|---|---|---|
| Frame | Wood framing | Wood-sided residential/commercial |
| JM | Joisted Masonry | Brick walls with wood roof |
| NC | Noncombustible | Metal buildings, concrete tilt-up, stucco over steel |
| MNC | Masonry Noncombustible | Brick/concrete block with steel structure |
| MFR | Modified Fire Resistive | Protected steel, fire-rated assemblies |
| FR | Fire Resistive | Concrete/steel high-rise construction |

### Building Exposures (Front/Rear/Left/Right)
| Field Pattern | Type | Description |
|---|---|---|
| `BuildingExposure_FrontDescription_{A/B}` | Text | Front exposure (e.g., "Comm bldg") |
| `BuildingExposure_FrontDistance_{A/B}` | Text | Distance in feet (e.g., "30") |
| `BuildingExposure_RearDescription_{A/B}` | Text | Rear exposure |
| `BuildingExposure_RearDistance_{A/B}` | Text | Distance in feet |
| `BuildingExposure_LeftDescription_{A/B}` | Text | Left exposure |
| `BuildingExposure_LeftDistance_{A/B}` | Text | Distance in feet |
| `BuildingExposure_RightDescription_{A/B}` | Text | Right exposure |
| `BuildingExposure_RightDistance_{A/B}` | Text | Distance in feet |

Common exposure descriptions: `Comm bldg`, `Open field`, `Road/resid`, `Parking/road`, `Open land`, `Comm warehouse`

### Fire Protection
| Field Pattern | Type | Description |
|---|---|---|
| `BuildingFireProtection_ProtectionClassCode_{A/B}` | Text | ISO protection class (1-10) |
| `BuildingFireProtection_FireDistrictCode_{A/B}` | Text | Fire district code |
| `BuildingFireProtection_FireDistrictName_{A/B}` | Text | Fire district name |
| `BuildingFireProtection_FireStationDistanceMileCount_{A/B}` | Text | Miles to fire station |
| `BuildingFireProtection_HydrantDistanceFeetCount_{A/B}` | Text | Feet to hydrant |
| `BuildingFireProtection_Alarm_SprinklerPercent_{A/B}` | Text | Sprinkler coverage % |
| `BuildingFireProtection_Alarm_CentralStationIndicator_{A/B}` | CheckBox | Central station alarm |
| `BuildingFireProtection_Alarm_LocalGongIndicator_{A/B}` | CheckBox | Local gong alarm |
| `BuildingFireProtection_Alarm_ManufacturerName_{A/B}` | Text | Alarm manufacturer |
| `BuildingFireProtection_Alarm_ProtectionDescription_{A/B}` | Text | Protection description |

### Coverage Rows (Section A: rows A–E, Section B: rows G–K)
Each row represents one coverage line. Pattern: `CommercialProperty_Premises_{Field}_{RowLetter}`

| Field Suffix | Type | Description |
|---|---|---|
| `_SubjectOfInsuranceCode_{row}` | Text | Subject (Bldg, BPP, BI, etc.) |
| `_LimitAmount_{row}` | Text | Coverage limit |
| `_CoinsurancePercent_{row}` | Text | Coinsurance % (typically 80 or 100) |
| `_ValuationCode_{row}` | Text | Valuation (RC = Replacement Cost, ACV) |
| `_CauseOfLossCode_{row}` | Text | Cause of loss (Basic, Broad, Spcl) |
| `_DeductibleAmount_{row}` | Text | Deductible amount |
| `_DeductibleTypeCode_{row}` | Text | Deductible type (Flat, %) |
| `_FormsAndConditions_{row}` | Text | Forms and conditions |
| `_InflationGuardPercent_{row}` | Text | Inflation guard % |
| `_BlanketNumber_{row}` | Text | Blanket number |

**Row letters:** Section A = A, B, C, D, E · Section B = G, H, I, J, K

### Mine Subsidence / Sinkhole
| Field Pattern | Type | Description |
|---|---|---|
| `CommercialPropertyCoverage_MineSubsidenceOption_NoIndicator_{A/B}` | CheckBox | Reject mine subsidence |
| `CommercialPropertyCoverage_MineSubsidence_YesIndicator_{A/B}` | CheckBox | Accept mine subsidence |
| `CommercialPropertyCoverage_MineSubsidence_LimitAmount_{A/B}` | Text | Mine subsidence limit |
| `CommercialPropertyCoverage_SinkHoleCollapse_NoIndicator_{A/B}` | CheckBox | Reject sinkhole |
| `CommercialPropertyCoverage_SinkHoleCollapse_YesIndicator_{A/B}` | CheckBox | Accept sinkhole |
| `CommercialPropertyCoverage_SinkHoleCollapse_LimitAmount_{A/B}` | Text | Sinkhole limit |

**TX rule:** Check "No" for both mine subsidence and sinkhole. FL: keep sinkhole options open.

### Equipment Breakdown
| Field Pattern | Type |
|---|---|
| `CommercialProperty_Premises_BreakdownOrContaminationIndicator_{A/B}` | CheckBox |

### Building Improvements
Pattern: `BuildingImprovement_{Type}Indicator_{A/B}` (CheckBox) and `BuildingImprovement_{Type}Year_{A/B}` (Text)

Types: `Heating`, `Plumbing`, `Roofing`, `Wiring`, `Other`

### Building Security / Alarms
| Field Pattern | Type |
|---|---|
| `Alarm_Burglar_CentralStationIndicator_{A/B}` | CheckBox |
| `Alarm_Burglar_CertificateIdentifier_{A/B}` | Text |
| `Alarm_Burglar_GradeCode_{A/B}` | Text |
| `Alarm_Burglar_ProtectionExtentCode_{A/B}` | Text |
| `Alarm_Burglar_WithKeysIndicator_{A/B}` | CheckBox |
| `Burglar_LocalGongIndicator_{A/B}` | CheckBox |
| `BuildingSecurity_GuardWatchmenCount_{A/B}` | Text |
| `BuildingSecurity_GuardWatchmenClockHourlyIndicator_{A/B}` | CheckBox |

### Wind Classification
| Field Pattern | Type |
|---|---|
| `CommercialStructure_WindClass_ResistiveIndicator_{A/B}` | CheckBox |
| `CommercialStructure_WindClass_SemiResistiveIndicator_{A/B}` | CheckBox |
| `CommercialStructure_WindClass_OtherIndicator_{A/B}` | CheckBox |
| `CommercialStructure_WindClass_OtherDescription_{A/B}` | Text |

### Heating
| Field Pattern | Type |
|---|---|
| `CommercialStructure_PrimaryHeat_BoilerIndicator_{A/B}` | CheckBox |
| `CommercialStructure_PrimaryHeat_SolidFuelIndicator_{A/B}` | CheckBox |
| `CommercialStructure_PrimaryHeat_OtherIndicator_{A/B}` | CheckBox |
| `CommercialStructure_PrimaryHeat_OtherDescription_{A/B}` | Text |
| `CommercialStructure_SecondaryHeat_*` | Same pattern |

### Building Features
| Field Pattern | Type |
|---|---|
| `BuildingFeatures_HistoricalPropertyIndicator_{A/B}` | CheckBox |
| `BuildingFeatures_SolidFuelHeaterIndicator_{A/B}` | CheckBox |
| `BuildingFeatures_SolidFuelHeaterInstallationDate_{A/B}` | Text |
| `BuildingFeatures_SolidFuelHeaterManufacturerName_{A/B}` | Text |

### Other Occupancies / Spoilage
| Field Pattern | Type |
|---|---|
| `BuildingOccupancy_OtherOccupanciesDescription_{A/B}` | Text |
| `CommercialProperty_Spoilage_LimitAmount_{A/B}` | Text |
| `CommercialProperty_Spoilage_DeductibleAmount_{A/B}` | Text |
| `CommercialProperty_Spoilage_PropertyDescription_{A/B}` | Text |
| `CommercialProperty_Spoilage_YesNoCode_{A/B}` | Text |
| `CommercialProperty_Spoilage_RefrigeratorMaintenanceCode_{A/B}` | Text |

### Additional Interest (Property Section)
| Field Pattern | Type |
|---|---|
| `AdditionalInterest_FullName_{A/B}` | Text |
| `AdditionalInterest_MailingAddress_LineOne_{A/B}` | Text |
| `AdditionalInterest_MailingAddress_CityName_{A/B}` | Text |
| `AdditionalInterest_MailingAddress_StateOrProvinceCode_{A/B}` | Text |
| `AdditionalInterest_MailingAddress_PostalCode_{A/B}` | Text |
| `AdditionalInterest_InterestRank_{A/B}` | Text |
| `AdditionalInterest_Interest_MortgageeIndicator_{A/B}` | CheckBox |
| `AdditionalInterest_Interest_LossPayeeIndicator_{A/B}` | CheckBox |
| `AdditionalInterest_Interest_LendersLossPayableIndicator_{A/B}` | CheckBox |
| `AdditionalInterest_Interest_OtherIndicator_{A/B}` | CheckBox |
| `AdditionalInterest_Interest_OtherDescription_{A/B}` | Text |
| `AdditionalInterest_CertificateRequiredIndicator_{A/B}` | CheckBox |

### Blanket Summary
| Field Name | Type |
|---|---|
| `CommercialProperty_Summary_BlanketNumberIdentifier_{A-D}` | Text |
| `CommercialProperty_Summary_BlanketLimitAmount_{A-D}` | Text |
| `CommercialCoverage_Summary_BlanketTypeDescription_{A-D}` | Text |

### Remarks
| Field Name | Type |
|---|---|
| `CommercialProperty_Premises_RemarkText_A` | Text (page 9) |
| `CommercialProperty_Premises_RemarkText_C` | Text (page 10) |
| `CommercialPropertyLineOfBusiness_RemarkText_A` | Text (page 10) |
| `CommercialProperty_Premises_OptionsDescription_{A/B}` | Text |

---

## Page 11 — Signatures (ACORD 140)

| Field Name | Type |
|---|---|
| `NamedInsured_Signature_A` | Text |
| `NamedInsured_SignatureDate_A` | Text |
| `Producer_AuthorizedRepresentative_Signature_A` | Text |
| `Producer_AuthorizedRepresentative_FullName_A` | Text |
| `Producer_CustomerIdentifier_A` | Text |
| `Producer_StateLicenseIdentifier_A` | Text |
| `Producer_NationalIdentifier_A` | Text |

---

## Common Checkbox Scenarios

### Property-Only Quote (Typical)
```json
{
    "checkboxes": {
        "ACORD_Transaction_Quote": true,
        "ACORD_Policy_Insured1_Type_LLC": true,
        "ACORD_Location1_Interest_Owner": true,
        "ACORD_LossHistory_None": true,
        "CommercialPropertyCoverage_MineSubsidenceOption_NoIndicator_A": true,
        "CommercialPropertyCoverage_SinkHoleCollapse_NoIndicator_A": true
    }
}
```

### Renewal with Equipment Breakdown
```json
{
    "checkboxes": {
        "ACORD_Transaction_Renew": true,
        "CommercialProperty_Premises_BreakdownOrContaminationIndicator_A": true
    }
}
```

---

## Extracting Field Names from Your Form

If your ACORD form edition differs, extract all field names:

```bash
python acord_filler.py --form your-blank.pdf --list-fields
```

This will print every field name, type, and page number.
