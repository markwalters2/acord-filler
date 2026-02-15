# ACORD Form Filling Rules — Learned from Mark Walters

## General Rules
- **Form completion date** = date of generation (today), auto-populated on every page
- **Agency box** = full name + address (Alliance Risk Insurance Services LLC, 250 W 57th St, Ste 1301, New York, NY 10107)
- **ACORD remarks field** = factual info ONLY. Never put broker opinions, valuation flags, or underwriting notes on the signed application. Those go in a **separate broker cover note**
- **General Info Q1-15** = Y/N text values drawn directly on the form (checkbox widgets don't accept text). Q4 (coverage terminated) = ALWAYS "N" unless explicitly told otherwise

## Prior Carrier Section
- Field names say "Auto" but they're generic columns — use the **Property column** (manually draw at x:355)
- Fill from current policy data: carrier, policy #, premium, eff/exp dates (prior year)

## ACORD 140 Property Section
- Each Premises Information section = ONE building at ONE location
- Page 9 (Section A, rows A-E) = Location 1
- Page 10 (Section B, rows G-K) = Location 2
- **Fill the header**: Premises #, Building #, Street Address, Bldg Description
- **Only use one row per building** unless multiple coverage types

## ISO Construction Classes
- Frame = wood framing
- JM = Joisted Masonry
- **NC = Noncombustible** (metal buildings, concrete tilt-up, stucco over steel)
- MNC = Masonry Noncombustible
- MFR = Modified Fire Resistive
- FR = Fire Resistive

### Construction ID from Imagery
- Metal warehouse + standing seam metal roof = **NC**
- Stucco/EIFS over solid walls + stone veneer = **NC**
- Wood siding, visible wood framing = Frame
- Brick exterior + steel/concrete = MNC or NC depending on structure

## Replacement Cost Benchmarks
- Light metal NC warehouse, slab-on-grade, non-union area (TX): ~$100-120/sqft is reasonable
- Heavier NC or union areas: $150-200/sqft
- Don't blindly trust online estimators (CoreLogic/Marshall & Swift) — they often assume heavier construction or union labor
- Always sanity check $/sqft before flagging valuation concerns

## Deductible Type
- Dollar amount deductible = **"Flat"**
- Percentage deductible = "%"

## Year Built / Stories / Basements
- Get year built from public records or satellite imagery age estimation
- Stories from street view / satellite shadow analysis
- **TX Gulf Coast = no basements** (high water table, clay soil, flood-prone). Always 0 unless told otherwise
- Same rule applies to most of coastal TX, LA, FL

## Square Footage from Satellite
- Use Google Maps satellite at zoom 19-20 with scale bar
- If buildings in a development are **cookie-cutter same style** = measure ANY one, they're all the same size
- Google Earth has a measure tool (more precise) if accessible
- RE/MAX / for-lease signs in street view sometimes state exact SF
- 1 story + no basement = footprint = total sqft

## Exposures (Front/Rear/Left/Right)
- Fill from satellite imagery
- Format: concise text + distance in feet (e.g., "Comm bldg" / "30")
- Must fit in small box at readable font size — no cheating with tiny fonts
- Common descriptions: Comm bldg, Open field, Road/resid, Parking/road, Open land, Comm warehouse
- Matters most in cities and wildfire areas, but always fill it out
- Estimate distances from satellite scale bar

## Checkboxes
- LLC, Quote, Renew, Owner interest = check when applicable
- Loss History None = check when no claims indicated
- Mine Subsidence Reject = check for TX (not IL/IN/KY/WV)
- Sinkhole Reject = check for TX (not FL)
- Equipment Breakdown = check when equip breakdown coverage is on the policy

## Supported Forms
- **ACORD 125/140** — Commercial Insurance Application + Property Section (`fill_acord.py` planned, currently inline script)
- **ACORD 37** — Statement of No Loss (`fill_acord37.py`, CLI + library)
  - 30 fields, 1 page, generic field names (Text1-Text30)
  - Field mappings in `acord37_mappings.json`
  - Blank form: `acord-37-blank.pdf`
  - Common use: policy reinstatement after cancellation remediation
  - Fill from JSON, flatten, OCR

## PDF Technical Notes
- **PyMuPDF (fitz)** widgets = the working approach for form filling
- Flatten by rendering pages as pixmaps then rebuilding as image PDF
- Draw text overlays (Y/N, prior carrier) AFTER flattening so they aren't hidden by widget rendering
- PyPDF2 and fillpdf+pdftk both fail on complex ACORD forms
- Skip GL pages (index 4-7) when policy is property-only

## Workflow
1. Extract policy data from source PDF (vision/OCR if scanned)
2. Search public records (county assessor, property listings) for building details
3. Pull satellite imagery — ID buildings, estimate sqft, construction, exposures
4. Pull street view — confirm stories, construction type, roof material
5. Fill ACORD form fields programmatically
6. Flatten to non-editable PDF
7. Append broker notes page (valuation flags, coverage gaps) — SEPARATE from signed app
8. Send for review

## ACORD 28 & 24 - Per Location Rule (PERMANENT)
- **ACORD 28 (Evidence of Commercial Property)**: Separate form for EACH location
- **ACORD 24 (Certificate of Property Insurance)**: Separate form for EACH location
- Exception: Blanket limits across locations can go on one form
- Rationale: Each location has different coverages/limits/deductibles, and different mortgagees/additional interests may apply per location
- Tenant locations: Note "No Building Coverage" prominently, show BPP as primary amount of insurance

## ACORD 28 Field Mapping Notes
- 120 fields across 2 pages (Allegany Group blank, 2006/07 version)
- Perils checkboxes: Check4=Basic, Check5=Broad, Check6=Special, Check7=Other
- Coverage YES/NO/N-A pattern: YES=Check(X) at x:262, NO=Check(X-1) at x:276, N/A=Check(X-2) at x:290
- BI/RV selection: Check8=Business Income, Check9=Rental Value
- Signature position: x:420, y:718, h:20 (inside Agent/Auth Rep box)
- Page 2 is remarks only (one big text field: F[0].P2[0].Evidence[0])

## ACORD 28 Signature & Checkbox Positions (FINAL)
- **Signature:** x:420, y:722, h:20 (auth rep line, NOT the Lender Servicing Agent field)
- **Building checkbox (manual X):** center (357, 252) — draw X with sz=4, width=1.2
- **BPP checkbox (manual X):** center (441, 252) — draw X with sz=4, width=1.2
- **Agent[0] field = Lender Servicing Agent** — leave BLANK unless there's an actual bank/lender
- **BI field rule:** Dollar limit OR months, NOT both. Months only for Actual Loss Sustained without a dollar cap.

## All Signature Positions (PERMANENT)
- ACORD 24: x:402, y:721, h:22
- ACORD 25: x:402, y:721, h:22
- ACORD 27: x:390, y:716, h:16
- ACORD 28: x:420, y:722, h:20
