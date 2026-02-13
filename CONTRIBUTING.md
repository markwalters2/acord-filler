# Contributing to acord-filler

Thanks for your interest in improving ACORD form automation! Here's how to help.

## How Field Mappings Work

ACORD forms are fillable PDFs with named form widgets. Each widget has a `field_name` that PyMuPDF can read and write. The field names are set by ACORD and vary by form edition.

The core workflow:
1. Open the blank PDF with `fitz.open()`
2. Iterate `page.widgets()` to find fields by name
3. Set `widget.field_value` and call `widget.update()`
4. Flatten by rendering pages as images (widgets don't survive standard flattening)

## Adding a New Form Type

To add support for a new ACORD form (e.g., ACORD 126 GL, ACORD 130 Workers' Comp):

1. **Get a blank fillable PDF** of the form
2. **Extract field names**: `python acord_filler.py --form new-blank.pdf --list-fields`
3. **Document the fields** in `FIELD_MAPPINGS.md` organized by page/section
4. **Add mapping logic** in `_build_field_data()` to translate structured JSON → field names
5. **Test** with real data and verify the output visually
6. **Note any workarounds** — some widgets don't behave (checkboxes that need text overlays, misnamed columns, etc.)

## Submitting Field Corrections

If you find a field name that's wrong, missing, or mapped to the wrong location:

1. Open an issue with:
   - Your ACORD form edition (check the footer)
   - The field name in question
   - What it should map to
   - Screenshot if possible
2. Or submit a PR updating `FIELD_MAPPINGS.md` and the corresponding code

## Known Quirks to Watch For

- **Checkbox widgets** sometimes don't accept text values — you may need to draw text overlays after flattening
- **Column naming** can be misleading (e.g., "Auto" columns used for Property data)
- **Form editions** change field names — always verify against your specific PDF
- **Multi-line text** fields may truncate — test with long values

## Code Style

- Python 3.9+
- Type hints where practical
- Comments explaining *why*, not just *what*
- Keep `acord_filler.py` as a single file for easy deployment

## Testing

```bash
# Verify field extraction works
python acord_filler.py --form blank.pdf --list-fields

# Test fill with example data
python acord_filler.py --input example_input.json --form blank.pdf --output test.pdf

# Visual inspection is the final test — open the PDF and check every field
```

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
