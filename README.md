# acord-filler

**Open-source CLI and Python library for programmatically filling ACORD insurance forms.**

Stop hand-filling ACORD forms. Feed in JSON, get back a flattened, OCR'd PDF ready for submission.

## Supported Forms

| Form | Description | Script | Fields |
|------|-------------|--------|--------|
| **ACORD 125/140** | Commercial Insurance Application + Property | `acord_filler.py` | 100+ |
| **ACORD 25** | Certificate of Liability Insurance | `fill_acord25.py` | 128 |
| **ACORD 24** | Certificate of Property Insurance | `fill_acord24.py` | 144 |
| **ACORD 37** | Statement of No Loss | `fill_acord37.py` | 30 |
| **ACORD 27** | Commercial Automobile Section | `fill_acord.py` | 51 |
| **ACORD 28** | Evidence of Commercial Property Insurance | `fill_acord.py` | 120 |
| **ACORD 50** | Real Estate Management & Lessor's Risk Report | `fill_acord.py` | varies |

## Features

- **Fill from JSON** - structured data in, professional PDF out
- **Flatten to non-editable PDF** - renders at 200dpi, rebuilds as image PDF
- **OCR text layer** - all text remains copy/pasteable via ocrmypdf + tesseract
- **Signature overlay** - place authorized representative signature from image file
- **Field mappings documented** - every field name, position, and workaround in FIELD_MAPPINGS.md
- **Known workarounds built in** - Y/N checkbox text overlay, prior carrier column offset, section headers

## Installation

```bash
pip install PyMuPDF ocrmypdf
# Also need tesseract: brew install tesseract (macOS) or apt install tesseract-ocr (Linux)
```

## Quick Start

### Certificate of Liability (ACORD 25)
```bash
python fill_acord25.py --input data.json --form acord-25-blank.pdf --output cert.pdf --signature sig.jpg
```

### Certificate of Property (ACORD 24)
```bash
python fill_acord24.py --input data.json --form acord-24-blank.pdf --output cert.pdf --signature sig.jpg
```

### Statement of No Loss (ACORD 37)
```bash
python fill_acord37.py --input data.json --form acord-37-blank.pdf --output nkll.pdf
```

### Commercial Application (ACORD 125/140)
```bash
python acord_filler.py --input data.json --form acord-125-140-blank.pdf --output application.pdf
```

### Commercial Auto Section (ACORD 27)
```bash
python fill_acord.py fill --blank acord-27-blank.pdf --data example_acord27.json --output auto_cert.pdf --flatten
```

### Evidence of Property Insurance (ACORD 28)
```bash
python fill_acord.py fill --blank acord-28-blank.pdf --data example_acord28.json --output evidence.pdf --flatten
```

### Real Estate Report (ACORD 50)
```bash
python fill_acord.py fill --blank acord-50-blank.pdf --data property_data.json --output report.pdf --flatten
```

## Python API

```python
from fill_acord25 import fill_acord25

data = {
    "insured_name": "Example Corp LLC",
    "gl_policy_number": "BOP-123456",
    "gl_each_occurrence": "1,000,000",
    "gl_general_agg": "2,000,000",
    # ... see example JSON files for full schema
}

result = fill_acord25(data, "acord-25-blank.pdf", "output.pdf", signature_path="sig.jpg")
print(f"Filled {result['text_fields']} fields")
```

## Blank Forms

You must supply your own blank ACORD PDF forms (copyrighted, cannot redistribute). Sources:
- Your agency management system (Applied, Vertafore)
- ACORD.org (member access)
- Various insurance carrier portals

## Known Workarounds (ACORD 125/140)

The commercial application has several quirks documented in FIELD_MAPPINGS.md:

1. **General Info Y/N boxes** - Checkbox widgets don't accept text values. Draw "Y"/"N" directly onto the flattened page at specific coordinates.
2. **Prior Carrier Property column** - Field names say "Auto" but the Property column has no widgets. Draw text manually at x:355.
3. **Premises sections** - Section A (rows A-E) = Location 1, Section B (rows G-K) = Location 2. Each has its own header block.
4. **GL pages** - If property-only, skip ACORD 126 pages entirely.

## File Reference

| File | Purpose |
|------|---------|
| `acord_filler.py` | ACORD 125/140 commercial application filler |
| `fill_acord.py` | General-purpose ACORD form filler (27, 28, 50, etc.) |
| `fill_acord25.py` | ACORD 25 certificate of liability filler |
| `fill_acord24.py` | ACORD 24 certificate of property filler |
| `fill_acord37.py` | ACORD 37 statement of no loss filler |
| `FIELD_MAPPINGS.md` | Complete field name reference (all forms) |
| `RULES.md` | Best practices guide for ACORD form filling |
| `example_input.json` | Example data for ACORD 125/140 |
| `example_acord25.json` | Example data for ACORD 25 |
| `example_acord24.json` | Example data for ACORD 24 |
| `example_acord37.json` | Example data for ACORD 37 |
| `example_acord27.json` | Example data for ACORD 27 |
| `example_acord28.json` | Example data for ACORD 28 |
| `acord37_mappings.json` | ACORD 37 field position reference |

## License

MIT - see LICENSE
