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

---

# ACORD 27 Field Mappings

**Form:** Commercial Automobile Section  
**Total Fields:** 51  
**Pages:** 1

## Header & Contact Information

| Field Name | Type | Description |
|---|---|---|
| `F[0].P1[0].Company[0]` | Text | Insurance company name |
| `F[0].P1[0].Date[0]` | Text | Form completion date |
| `F[0].P1[0].Phone[0]` | Text | Contact phone number |
| `F[0].P1[0].Fax[0]` | Text | Contact fax number |

## Location Information

| Field Name | Type | Description |
|---|---|---|
| `F[0].P1[0].LOC[0]` | Text | Primary location address line 1 |
| `F[0].P1[0].LOC1[0]` | Text | Location address line 2 |
| `F[0].P1[0].LOC2[0]` | Text | Location address line 3 |
| `F[0].P1[0].LOC3[0]` | Text | Location address line 4 |
| `F[0].P1[0].LOC4[0]` | Text | Location address line 5 |
| `F[0].P1[0].LOC5[0]` | Text | Location address line 6 |
| `F[0].P1[0].LOC6[0]` | Text | Location address line 7 |
| `F[0].P1[0].LOC7[0]` | Text | Location address line 8 |

## Vehicle & Coverage Information

| Field Name | Type | Description |
|---|---|---|
| `F[0].P1[0].NOAUTOS[0]` | Text | Number of autos/vehicles |
| `F[0].P1[0].COVERAGE1[0]` | Text | Primary coverage type |
| `F[0].P1[0].COVERAGE11[0]` | Text | Secondary coverage type |
| `F[0].P1[0].COVERAGE12[0]` | Text | Additional coverage type |

## Coverage Amounts & Deductibles (Array Fields)

**Amount of Insurance** - 8 fields indexed [0] through [7]:

| Field Name | Description |
|---|---|
| `F[0].P1[0].amtinsur[0-7]` | Coverage limit amounts |

**Deductibles** - 8 fields indexed [0] through [7]:

| Field Name | Description |
|---|---|
| `F[0].P1[0].deduct[0-7]` | Deductible amounts |

**Covered Perils** - 8 fields indexed [0] through [7]:

| Field Name | Description |
|---|---|
| `F[0].P1[0].covperils1[0-7]` | Perils covered (e.g., Comprehensive, Collision, Specified) |

## Dates

| Field Name | Type | Description |
|---|---|---|
| `F[0].P1[0].Date1[0]` | Text | Policy effective date |
| `F[0].P1[0].Date2[0]` | Text | Policy expiration date |
| `F[0].P1[0].Date3[0]` | Text | Additional date field |

## Additional Information

| Field Name | Type | Description |
|---|---|---|
| `F[0].P1[0].addlint[0]` | Text | Additional interests/insured parties |
| `F[0].P1[0].remarks[0]` | Text | Remarks and additional information |

## CA Symbols (Checkboxes)

| Field Name | Type | Description |
|---|---|---|
| `F[0].P1[0].CASymbols21[0]` | CheckBox | CA Symbol 21 |
| `F[0].P1[0].CASymbols211[0]` | CheckBox | CA Symbol 21 variant 1 |
| `F[0].P1[0].CASymbols212[0]` | CheckBox | CA Symbol 21 variant 2 |
| `F[0].P1[0].CASymbols213[0]` | CheckBox | CA Symbol 21 variant 3 |
| `F[0].P1[0].CASymbols214[0]` | CheckBox | CA Symbol 21 variant 4 |

## Utility Fields

| Field Name | Type | Description |
|---|---|---|
| `F[0].P1[0].ClearAll[0]` | Button | Form clear button (ignore) |

---

# ACORD 28 Field Mappings

**Form:** Evidence of Commercial Property Insurance  
**Total Fields:** 120  
**Pages:** 2

> **Important:** ACORD 28 should be filled **per location**. Each location with different coverages, limits, or mortgagees should have its own ACORD 28 form.

## Page 1 — Primary Information

### Producer/Agent Information

| Field Name | Type | Description |
|---|---|---|
| `F[0].P1[0].Company[0]` | Text | Insurance company name |
| `F[0].P1[0].Producer[0]` | Text | Producer/agency name |
| `F[0].P1[0].Contact[0]` | Text | Producer contact person |
| `F[0].P1[0].Phone[0]` | Text | Producer phone |
| `F[0].P1[0].Fax[0]` | Text | Producer fax |
| `F[0].P1[0].Email[0]` | Text | Producer email |
| `F[0].P1[0].AgencyID[0]` | Text | Agency ID number |
| `F[0].P1[0].Agent[0]` | Text | Lender servicing agent (leave blank unless actual lender agent) |
| `F[0].P1[0].Code[0]` | Text | Producer code |
| `F[0].P1[0].Subcode[0]` | Text | Producer subcode |
| `F[0].P1[0].Naic[0]` | Text | NAIC code |

### Policy Information

| Field Name | Type | Description |
|---|---|---|
| `F[0].P1[0].Policy[0]` | Text | Policy number |
| `F[0].P1[0].Type[0]` | Text | Policy type |
| `F[0].P1[0].Date[0]` | Text | Form completion date |
| `F[0].P1[0].Date1[0]` | Text | Policy effective date |
| `F[0].P1[0].Date2[0]` | Text | Policy expiration date |
| `F[0].P1[0].Date3[0]` | Text | Additional date field |
| `F[0].P1[0].Days[0]` | Text | Number of days |

### Insured & Location

| Field Name | Type | Description |
|---|---|---|
| `F[0].P1[0].Named[0]` | Text | Named insured |
| `F[0].P1[0].Location[0]` | Text | Property location address (multi-line) |
| `F[0].P1[0].LOC21[0]` | Text | Additional location info |

### Mortgagee/Loss Payee

| Field Name | Type | Description |
|---|---|---|
| `F[0].P1[0].NameAdd[0]` | Text | Mortgagee name and address |
| `F[0].P1[0].Loan[0]` | Text | Loan/mortgage number |

### Coverage Limits

| Field Name | Type | Description |
|---|---|---|
| `F[0].P1[0].Limit1[0]` | Text | Building limit |
| `F[0].P1[0].Limit2[0]` | Text | BPP limit |
| `F[0].P1[0].Limit3[0]` | Text | Business Income/Extra Expense |
| `F[0].P1[0].Limit4[0]` | Text | Additional limit |
| `F[0].P1[0].Limit6[0]` | Text | Additional limit |
| `F[0].P1[0].Limit7[0]` | Text | Additional limit |
| `F[0].P1[0].Limit8[0]` | Text | Additional limit |
| `F[0].P1[0].Limit9[0]` | Text | Additional limit |
| `F[0].P1[0].Amount[0]` | Text | Total amount of insurance |
| `F[0].P1[0].Value[0]` | Text | Property value |

### Deductibles

| Field Name | Type | Description |
|---|---|---|
| `F[0].P1[0].Deductible[0]` | Text | Primary deductible |
| `F[0].P1[0].Deductible2[0]` | Text | Secondary deductible |
| `F[0].P1[0].Ded3[0]` | Text | Deductible 3 |
| `F[0].P1[0].Ded4[0]` | Text | Deductible 4 |
| `F[0].P1[0].Ded5[0]` | Text | Deductible 5 |
| `F[0].P1[0].Ded6[0]` | Text | Deductible 6 |
| `F[0].P1[0].Ded7[0]` | Text | Deductible 7 |
| `F[0].P1[0].Ded8[0]` | Text | Deductible 8 |
| `F[0].P1[0].Percent[0]` | Text | Percentage deductible |

### Business Income

| Field Name | Type | Description |
|---|---|---|
| `F[0].P1[0].Months[0]` | Text | Business income months (use for ALS without dollar cap) |

### Other/Additional

| Field Name | Type | Description |
|---|---|---|
| `F[0].P1[0].Other[0]` | Text | Other coverage info |
| `F[0].P1[0].Other2[0]` | Text | Other coverage info |
| `F[0].P1[0].Other3[0]` | Text | Other coverage info |
| `F[0].P1[0].Additional[0]` | Text | Additional information |

## Checkboxes (Page 1)

**Key Checkbox Mappings:**

| Field Name | Purpose |
|---|---|
| `F[0].P1[0].Check4[0]` | Perils: Basic |
| `F[0].P1[0].Check5[0]` | Perils: Broad |
| `F[0].P1[0].Check6[0]` | Perils: Special |
| `F[0].P1[0].Check7[0]` | Perils: Other |
| `F[0].P1[0].Check8[0]` | Business Income (vs Rental Value) |
| `F[0].P1[0].Check9[0]` | Rental Value (vs Business Income) |

**Coverage YES/NO/N-A Pattern:**

Many coverages follow a three-checkbox pattern at specific x-coordinates:
- **YES** = Check box at x:262
- **NO** = Check box at x:276
- **N/A** = Check box at x:290

The checkboxes are numbered Check1 through Check70, with Check80 as an additional box. Specific mappings depend on form layout and should be validated against your blank form version.

**All Checkboxes:**

`Check1` through `Check70`, plus `Check80` (70+ checkbox fields total)

## Page 2 — Remarks

| Field Name | Type | Description |
|---|---|---|
| `F[0].P2[0].Evidence[0]` | Text | Evidence of insurance remarks (large text field) |

## Utility Fields

| Field Name | Type | Description |
|---|---|---|
| `F[0].P1[0].ClearAll[0]` | Button | Page 1 form clear button (ignore) |
| `F[0].P2[0].ClearAll[0]` | Button | Page 2 form clear button (ignore) |

## Signature Placement (Manual Overlay)

When adding signatures programmatically after flattening:

- **ACORD 28 signature position:** x:420, y:722, h:20 (Authorized Representative line)
- Place signature image file at this coordinate after PDF is flattened

## Manual Checkbox Coordinates

Some checkboxes may require manual drawing if not properly mapped:

- **Building checkbox:** center (357, 252) — draw X with sz=4, width=1.2
- **BPP checkbox:** center (441, 252) — draw X with sz=4, width=1.2

## Notes

- ACORD 28 checkbox field names (Check1-Check70) are generic and positions vary by form edition
- Always validate checkbox mappings against your specific blank form version
- Use `fill_acord.py list acord-28-blank.pdf` to inspect field positions
- Agent[0] field is for "Lender Servicing Agent" — leave blank unless there's an actual bank/lender servicing agent
- **BI months rule:** Use Months field only for Actual Loss Sustained coverage without a dollar cap; otherwise use Limit3

