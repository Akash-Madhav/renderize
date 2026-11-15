#!/usr/bin/env python3
"""
extract_pdf.py - Stage 1: Vector Extraction & Parsing

Extracts drawing primitives (lines, rectangles, curves), color fills, strokes,
and dimension annotations from an architectural vector PDF using PyMuPDF.
"""

import argparse
import json
import os
import sys
import pymupdf


def extract_pdf_data(pdf_path, output_json_path=None):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"Input PDF not found: {pdf_path}")

    doc = pymupdf.open(pdf_path)
    print(f"[+] Loaded PDF: {pdf_path} (Pages: {len(doc)})")

    extracted_pages = []

    for page_idx, page in enumerate(doc):
        rect = page.rect
        width = rect.width
        height = rect.height

        drawings = page.get_drawings()
        print(f"  - Page {page_idx}: Dimensions {width:.1f} x {height:.1f} pts, Vector Paths: {len(drawings)}")

        parsed_paths = []
        for path in drawings:
            color = path.get("color")
            fill = path.get("fill")
            stroke_width = path.get("width", 0.0)

            items_list = []
            for item in path.get("items", []):
                cmd = item[0]
                if cmd == "l":  # line
                    p1 = [float(item[1].x), float(item[1].y)]
                    p2 = [float(item[2].x), float(item[2].y)]
                    items_list.append(["line", p1, p2])
                elif cmd == "re":  # rect
                    r = item[1]
                    items_list.append(["rect", [float(r.x0), float(r.y0), float(r.x1), float(r.y1)]])
                elif cmd == "c":  # curve (bezier)
                    p1 = [float(item[1].x), float(item[1].y)]
                    p2 = [float(item[2].x), float(item[2].y)]
                    p3 = [float(item[3].x), float(item[3].y)]
                    p4 = [float(item[4].x), float(item[4].y)]
                    items_list.append(["curve", p1, p2, p3, p4])

            parsed_paths.append({
                "stroke_color": list(color) if color else None,
                "fill_color": list(fill) if fill else None,
                "width": float(stroke_width) if stroke_width else 0.0,
                "items": items_list
            })

        # Extract textual annotations (dimensions, labels)
        text_words = page.get_text("words")
        annotations = []
        for word in text_words:
            # word structure: (x0, y0, x1, y1, "word_string", block_no, line_no, word_no)
            annotations.append({
                "text": word[4],
                "bbox": [float(word[0]), float(word[1]), float(word[2]), float(word[3])],
                "block": word[5]
            })

        extracted_pages.append({
            "page_index": page_idx,
            "width_pts": float(width),
            "height_pts": float(height),
            "paths_count": len(parsed_paths),
            "paths": parsed_paths,
            "annotations_count": len(annotations),
            "annotations": annotations
        })

    result = {
        "source_file": os.path.basename(pdf_path),
        "source_path": os.path.abspath(pdf_path),
        "total_pages": len(doc),
        "pages": extracted_pages
    }

    if output_json_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_json_path)), exist_ok=True)
        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        print(f"[✓] Extracted data saved to: {output_json_path}")

    return result


def main():
    parser = argparse.ArgumentParser(description="Extract architectural drawing elements from vector PDF.")
    parser.add_argument("--input", "-i", required=True, help="Path to input architectural PDF")
    parser.add_argument("--output", "-o", default=None, help="Path to output JSON file")

    args = parser.parse_args()

    out_file = args.output
    if not out_file:
        base = os.path.splitext(args.input)[0]
        out_file = f"{base}_extracted.json"

    extract_pdf_data(args.input, out_file)


if __name__ == "__main__":
    main()
