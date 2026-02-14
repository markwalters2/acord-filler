#!/usr/bin/env python3
"""
ACORD Form Filler — Fill actual ACORD 125/126/140 fillable PDFs with policy data.

Usage:
    python fill_acord.py --blank acord-125-126-140-blank.pdf --data policy_data.json --output filled.pdf [--flatten]

Or import and use programmatically:
    from fill_acord import fill_acord_form
    fill_acord_form(blank_path, field_data, output_path, flatten=True)
"""

import fitz  # PyMuPDF
import json
import argparse
import os


def list_fields(blank_pdf_path):
    """List all fillable field names in a blank ACORD PDF."""
    doc = fitz.open(blank_pdf_path)
    fields = {}
    for page_num, page in enumerate(doc):
        for widget in page.widgets():
            fields[widget.field_name] = {
                "page": page_num + 1,
                "type": widget.field_type_string,
                "value": widget.field_value or "",
            }
    doc.close()
    return fields


def fill_acord_form(blank_pdf_path, field_data, output_path, flatten=True, dpi=200):
    """
    Fill an ACORD PDF form with provided field data.
    
    Args:
        blank_pdf_path: Path to blank fillable ACORD PDF
        field_data: Dict of {field_name: value} to fill
        output_path: Where to save the filled PDF
        flatten: If True, render to images (non-editable). If False, keep editable.
        dpi: Resolution for flattening (default 200)
    
    Returns:
        Dict with stats: filled_count, total_fields, skipped_fields
    """
    doc = fitz.open(blank_pdf_path)
    
    filled_count = 0
    skipped = []
    
    # Fill form fields
    for page in doc:
        for widget in page.widgets():
            fname = widget.field_name
            if fname in field_data:
                widget.field_value = str(field_data[fname])
                widget.update()
                filled_count += 1
    
    # Check for fields in data that weren't found in form
    all_field_names = set()
    for page in doc:
        for widget in page.widgets():
            all_field_names.add(widget.field_name)
    
    for key in field_data:
        if key not in all_field_names:
            skipped.append(key)
    
    if flatten:
        # Render to images and rebuild as non-editable PDF
        doc.save("/tmp/_acord_temp_filled.pdf")
        doc.close()
        
        src = fitz.open("/tmp/_acord_temp_filled.pdf")
        dst = fitz.open()
        for page in src:
            pix = page.get_pixmap(dpi=dpi)
            img_page = dst.new_page(width=page.rect.width, height=page.rect.height)
            img_page.insert_image(page.rect, pixmap=pix)
        
        dst.save(output_path, deflate=True)
        dst.close()
        src.close()
        
        # Clean up temp
        os.remove("/tmp/_acord_temp_filled.pdf")
    else:
        doc.save(output_path)
        doc.close()
    
    return {
        "filled_count": filled_count,
        "total_fields": len(all_field_names),
        "skipped_fields": skipped,
    }


def add_broker_notes(pdf_path, notes, output_path=None):
    """
    Append a broker notes page to an existing PDF.
    
    Args:
        pdf_path: Path to the PDF to append to
        notes: List of (title, body) tuples for each flag
        output_path: Where to save. If None, overwrites pdf_path.
    """
    if output_path is None:
        output_path = pdf_path
    
    doc = fitz.open(pdf_path)
    
    # Create notes page
    notes_doc = fitz.open()
    page = notes_doc.new_page(width=612, height=792)
    
    # Title
    page.insert_text(
        (50, 50),
        "BROKER NOTES — VALUATION & COVERAGE FLAGS",
        fontsize=14, fontname="helv", color=(0.2, 0.2, 0.6)
    )
    
    y = 80
    for title, body in notes:
        # Calculate box height
        lines_needed = len(body) // 90 + 2
        box_height = 28 + lines_needed * 11 + 8
        
        # Check page break
        if y + box_height > 750:
            page = notes_doc.new_page(width=612, height=792)
            y = 50
        
        # Amber background box
        rect = fitz.Rect(40, y, 572, y + box_height)
        page.draw_rect(rect, color=(0.8, 0.6, 0.1), fill=(1.0, 0.95, 0.85), width=0.5)
        
        # Title
        page.insert_text(
            (48, y + 14),
            "⚠️ " + title,
            fontsize=9, fontname="helv", color=(0.6, 0.3, 0.0)
        )
        
        # Body text — word wrap
        words = body.split()
        line = ""
        ty = y + 28
        for w in words:
            test = line + " " + w if line else w
            if len(test) > 90:
                page.insert_text((52, ty), line, fontsize=8, fontname="helv", color=(0.2, 0.2, 0.2))
                ty += 11
                line = w
            else:
                line = test
        if line:
            page.insert_text((52, ty), line, fontsize=8, fontname="helv", color=(0.2, 0.2, 0.2))
        
        y += box_height + 8
    
    # Merge
    doc.insert_pdf(notes_doc)
    doc.save(output_path, deflate=True)
    doc.close()
    notes_doc.close()


def extract_policy_pages(pdf_path, output_dir, dpi=200):
    """
    Convert PDF pages to PNG images for vision/OCR extraction.
    
    Args:
        pdf_path: Path to the policy PDF
        output_dir: Directory to save page images
        dpi: Resolution (default 200)
    
    Returns:
        List of output image paths
    """
    os.makedirs(output_dir, exist_ok=True)
    doc = fitz.open(pdf_path)
    paths = []
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=dpi)
        out = os.path.join(output_dir, f"page-{i+1}.png")
        pix.save(out)
        paths.append(out)
    doc.close()
    return paths


# --- CLI ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ACORD Form Filler")
    sub = parser.add_subparsers(dest="command")
    
    # List fields
    ls = sub.add_parser("list", help="List all form fields in a blank ACORD PDF")
    ls.add_argument("blank", help="Path to blank ACORD PDF")
    
    # Fill form
    fill = sub.add_parser("fill", help="Fill ACORD form with data")
    fill.add_argument("--blank", required=True, help="Path to blank ACORD PDF")
    fill.add_argument("--data", required=True, help="JSON file with field_name: value pairs")
    fill.add_argument("--output", required=True, help="Output PDF path")
    fill.add_argument("--flatten", action="store_true", help="Flatten to non-editable")
    fill.add_argument("--dpi", type=int, default=200, help="DPI for flattening")
    
    # Extract pages
    ext = sub.add_parser("extract", help="Extract PDF pages as images for OCR")
    ext.add_argument("pdf", help="Path to policy PDF")
    ext.add_argument("--output-dir", default="./pages", help="Output directory")
    ext.add_argument("--dpi", type=int, default=200)
    
    args = parser.parse_args()
    
    if args.command == "list":
        fields = list_fields(args.blank)
        print(f"Total fields: {len(fields)}\n")
        for name in sorted(fields.keys()):
            f = fields[name]
            print(f"  Page {f['page']} | {f['type']:10s} | {name}")
    
    elif args.command == "fill":
        with open(args.data) as f:
            field_data = json.load(f)
        result = fill_acord_form(args.blank, field_data, args.output, flatten=args.flatten, dpi=args.dpi)
        print(f"Filled {result['filled_count']} of {result['total_fields']} fields")
        if result['skipped_fields']:
            print(f"Skipped (not found in form): {result['skipped_fields']}")
        print(f"Saved to {args.output}")
    
    elif args.command == "extract":
        paths = extract_policy_pages(args.pdf, args.output_dir, args.dpi)
        print(f"Extracted {len(paths)} pages to {args.output_dir}")
    
    else:
        parser.print_help()
