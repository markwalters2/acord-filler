# ACORD Form Filler

Open-source Python tools for filling ACORD insurance forms programmatically. Upload a policy, map the fields, get a filled, flattened PDF.

**Live demo:** [acord-demo.vercel.app](https://acord-demo.vercel.app)

## Supported Forms

| Form | Description | Fields |
|------|-------------|--------|
| ACORD 25 | Certificate of Liability Insurance | 128 |
| ACORD 24 | Certificate of Property Insurance | 144 |
| ACORD 28 | Evidence of Commercial Property | 120 |
| ACORD 125/140 | Commercial Insurance Application | 924 |
| ACORD 27 | Evidence of Property Insurance | 51 |
| ACORD 37 | Statement of No Loss | 30 |
| ACORD 50 | Property Loss Notice | 50+ |

## Quick Start

```bash
pip install pymupdf
python fill_acord.py acord-25-blank.pdf example_acord25.json output.pdf --flatten
```

## Multi-Carrier Support

Real certificates reference multiple carriers. GL with Hartford, Auto with Travelers, WC with a state fund. The `map_acord25.py` module handles this:

```python
from map_acord25 import map_to_acord25
from fill_acord import fill_acord_form
import json

with open("example_multicarrier.json") as f:
    data = json.load(f)

fields = map_to_acord25(
    policy_data={
        "insured": data["insured"],
        "insurers": data["insurers"],
        "coverages": data["coverages"]
    },
    cert_holder=data["cert_holder"],
    agency=data["agency"]
)

fill_acord_form("acord-25-blank.pdf", fields, "output.pdf", flatten=True)
```

Each coverage line gets its own:
- **Insurer letter** (A-E) mapped to a carrier in the insurer table
- **Policy number**
- **Effective/expiration dates**

See `example_multicarrier.json` for the full data structure.

## How It Works

1. **`fill_acord.py`** — Core form filler. Takes a blank ACORD PDF, a field mapping dict, and outputs a filled PDF. Supports flattening (rasterize to prevent editing).

2. **`map_acord25.py`** — Maps structured policy data to ACORD 25 field names. Handles multi-carrier insurer table, per-line dates, coverage toggles, cert holder requirements (AI/WOS/P&NC), and description of operations.

3. **Blank PDFs** — Fillable ACORD forms with mapped field names. Field names follow the pattern: `F[0].P1[0].FieldName_A[0]`

## Field Mapping Reference

See `FIELD_MAPPINGS.md` for the complete field name reference for each form type.

See `RULES.md` for learned rules about field placement, signature coordinates, and edge cases.

## Examples

| File | Description |
|------|-------------|
| `example_multicarrier.json` | Multi-carrier ACORD 25 (4 insurers, 4 coverage lines) |
| `example_acord25.json` | Single-carrier ACORD 25 |
| `example_acord24.json` | ACORD 24 property certificate |
| `example_acord28.json` | ACORD 28 evidence of property |
| `example_acord27.json` | ACORD 27 evidence of insurance |
| `example_acord37.json` | ACORD 37 statement of no loss |
| `example_input.json` | ACORD 125/140 commercial application |

## Flattening

By default, output PDFs have editable form fields. Use `--flatten` to rasterize the output. This prevents tampering and produces print-ready PDFs.

```bash
python fill_acord.py acord-25-blank.pdf data.json output.pdf --flatten
```

## Requirements

- Python 3.8+
- PyMuPDF (`pip install pymupdf`)

## License

MIT

## Built By

[Mark Walters, CPCU](https://www.linkedin.com/in/markwalterscpcu) — Alliance Risk Insurance Services
