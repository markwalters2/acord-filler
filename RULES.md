# ACORD Form Filling Rules — Best Practices Guide

## General Rules
- **Form completion date** = date of generation (today), auto-populated on every page
- **Agency box** = full name + address of your agency
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
- **Frame** = wood framing
- **JM** = Joisted Masonry
- **NC** = Noncombustible (metal buildings, concrete tilt-up, stucco over steel)
- **MNC** = Masonry Noncombustible
- **MFR** = Modified Fire Resistive
- **FR** = Fire Resistive

### Construction ID from Imagery
- Metal warehouse + standing seam metal roof = **NC**
- Stucco/EIFS over solid walls + stone veneer = **NC**
- Wood siding, visible wood framing = Frame
- Brick exterior + steel/concrete = MNC or NC depending on structure

## Replacement Cost Benchmarks
- Light metal NC warehouse, slab-on-grade, non-union area: ~$100-120/sqft is reasonable
- Heavier NC or union areas: $150-200/sqft
- Don't blindly trust online estimators (CoreLogic/Marshall & Swift) — they often assume heavier construction or union labor
- Always sanity check $/sqft before flagging valuation concerns

## Deductible Type
- Dollar amount deductible = **"Flat"**
- Percentage deductible = "%"

## Year Built / Stories / Basements
- Get year built from public records or satellite imagery age estimation
- Stories from street view / satellite shadow analysis
- **Coastal areas (TX Gulf, FL, LA)** = generally no basements (high water table, clay soil, flood-prone). Always 0 unless verified otherwise
- Interior/northern states may have basements — verify from property records or imagery

## Square Footage from Satellite
- Use Google Maps satellite at zoom 19-20 with scale bar
- If buildings in a development are **cookie-cutter same style** = measure ANY one, they're all the same size
- Google Earth has a measure tool (more precise) if accessible
- For-sale/for-lease signs in street view sometimes state exact SF
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
- Mine Subsidence Reject = check for regions without subsidence risk (not IL/IN/KY/WV/PA)
- Sinkhole Reject = check for regions without sinkhole risk (not FL)
- Equipment Breakdown = check when equipment breakdown coverage is on the policy

## Supported Forms
- **ACORD 125/140** — Commercial Insurance Application + Property Section
- **ACORD 37** — Statement of No Loss (30 fields, 1 page)
  - Common use: policy reinstatement after cancellation remediation
- **ACORD 24** — Certificate of Property Insurance (per-location)
- **ACORD 25** — Certificate of Liability Insurance
- **ACORD 27** — Commercial Automobile Section (51 fields, 1 page)
- **ACORD 28** — Evidence of Commercial Property Insurance (120 fields, 2 pages)
- **ACORD 50** — Real Estate Management & Lessor's Risk Report

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

## ACORD 28 & 24 - Per Location Rule
- **ACORD 28 (Evidence of Commercial Property)**: Separate form for EACH location
- **ACORD 24 (Certificate of Property Insurance)**: Separate form for EACH location
- Exception: Blanket limits across locations can go on one form
- Rationale: Each location has different coverages/limits/deductibles, and different mortgagees/additional interests may apply per location
- Tenant locations: Note "No Building Coverage" prominently, show BPP as primary amount of insurance

## ACORD 28 Field Mapping Notes
- 120 fields across 2 pages
- Perils checkboxes: Check4=Basic, Check5=Broad, Check6=Special, Check7=Other
- Coverage YES/NO/N-A pattern: YES=Check(X) at x:262, NO=Check(X-1) at x:276, N/A=Check(X-2) at x:290
- BI/RV selection: Check8=Business Income, Check9=Rental Value
- Signature position: x:420, y:722, h:20 (auth rep line)
- Page 2 is remarks only (one big text field: F[0].P2[0].Evidence[0])

## ACORD 28 Checkbox Positions
- **Building checkbox (manual X):** center (357, 252) — draw X with sz=4, width=1.2
- **BPP checkbox (manual X):** center (441, 252) — draw X with sz=4, width=1.2
- **Agent[0] field** = Lender Servicing Agent — leave BLANK unless there's an actual bank/lender
- **BI field rule:** Dollar limit OR months, NOT both. Months only for Actual Loss Sustained without a dollar cap.

## Form-Specific Signature Positions
- **ACORD 24:** x:402, y:721, h:22
- **ACORD 25:** x:402, y:721, h:22
- **ACORD 27:** x:390, y:716, h:16
- **ACORD 28:** x:420, y:722, h:20
- **ACORD 37:** (varies by blank form version)

## Tips for Automation
- Always validate field names against blank form before filling
- Use `fill_acord.py list` command to inspect all fields in a blank PDF
- Flatten PDFs to prevent post-submission editing
- Maintain separate mapping JSON files for forms with generic field names (Text1, Text2, etc.)
- Test signature overlay positioning on sample forms before production use
- Keep blank forms version-controlled — ACORD updates forms periodically
