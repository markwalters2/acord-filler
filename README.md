# acord-filler

**Open-source CLI and Python library for programmatically filling ACORD 125/140 insurance forms.**

Stop hand-filling ACORD applications. Feed in JSON, get back a flattened, OCR'd PDF ready for submission.

## Features

- 📝 **Fill from JSON** — structured input for insured info, locations, coverages, exposures, prior carrier, and more
- 📄 **ACORD 125 (pages 1–4)** — agency, insured, locations, general info, prior carrier, loss history
- 🏢 **ACORD 140 (pages 9–10)** — property section with construction, exposures, coverage rows, protection class
- 🔒 **Flatten to non-editable PDF** — renders pages as 200 DPI images, rebuilds as image PDF
- 🔍 **OCR text layer** — via `ocrmypdf` for copy/paste and search
- 📋 **Known workaround handling** — Prior Carrier "Property" column, General Info Y/N checkboxes, and more
- 🏗️ **Multiple locations** — Section A (rows A–E) = Location 1, Section B (rows G–K) = Location 2
- 📑 **Broker notes** — optional separate PDF for valuation flags and coverage gaps (never on the signed app)
- 📖 **924 field names documented** — see [FIELD_MAPPINGS.md](FIELD_MAPPINGS.md)

## Installation

```bash
pip install -r requirements.txt
```

Requires Python 3.9+.

## Quick Start

### CLI

```bash
# Fill and flatten
python acord_filler.py --input data.json --form blank-acord.pdf --output filled.pdf

# Fill without flattening (editable)
python acord_filler.py --input data.json --form blank-acord.pdf --output filled.pdf --no-flatten

# Fill with OCR
python acord_filler.py --input data.json --form blank-acord.pdf --output filled.pdf --ocr

# Generate broker notes as separate PDF
python acord_filler.py --input data.json --form blank-acord.pdf --output filled.pdf --broker-notes notes.pdf

# List all field names in a blank form
python acord_filler.py --form blank-acord.pdf --list-fields
```

### Python API

```python
from acord_filler import fill_acord

result = fill_acord(
    form_path="blank-acord.pdf",
    input_path="data.json",
    output_path="filled.pdf",
    flatten=True,
    ocr=True,
    broker_notes_path="notes.pdf",
)

print(f"Filled {result['filled_count']} of {result['total_fields']} fields")
```

## Input Format

See [`example_input.json`](example_input.json) for the full schema. Key sections:

```json
{
    "ACORD_AgencyName": "Your Agency\n123 Main St\nCity, ST 00000",
    "ACORD_CarrierName": "Carrier Name",
    "ACORD_PolicyNumber": "POL-000000",
    "ACORD_Policy_Insured1_Name": "Insured LLC",
    "locations": {
        "loc1": {
            "address": "123 Main St, City, TX 77000",
            "sqft": 6000, "stories": 1, "construction": "NC",
            "limit": 1000000, "coinsurance": 80, "valuation": "RC",
            "exposures": { "front": {"desc": "Comm bldg", "dist": "30"}, ... }
        }
    },
    "prior_carrier": { "carrier": "...", "policy_number": "...", "premium": "..." },
    "general_info_all_no": true,
    "broker_notes": ["Note 1", "Note 2"]
}
```

## Field Mapping Reference

See **[FIELD_MAPPINGS.md](FIELD_MAPPINGS.md)** for the complete list of all 924 ACORD 125/140 field names, organized by page and section, with known workarounds documented.

## ⚠️ Blank Form Required

You must supply your own blank ACORD 125/126/140 PDF. ACORD forms are copyrighted and cannot be redistributed. You can obtain them from:

- Your agency management system
- [ACORD.org](https://www.acord.org) (member access)
- Your carrier or MGA portal

## Known Workarounds

These are quirks in the ACORD fillable PDF that the tool handles automatically:

1. **Prior Carrier "Property" column** — The field names say "Auto" but the columns are generic. Property data is drawn manually at x:355 after the widget fill.

2. **General Info Y/N** — Checkbox widgets don't accept text values. Y/N values are drawn as text overlays at specific coordinates after flattening.

3. **Flattening** — Standard PDF flattening breaks widget rendering. Instead, each page is rendered as a 200 DPI pixmap and rebuilt as an image PDF.

## Built By

**[Alliance Risk Insurance Services LLC](https://alliancerisk.com)**
250 West 57th Street, Suite 1301, New York, NY 10107

## License

MIT — see [LICENSE](LICENSE)
