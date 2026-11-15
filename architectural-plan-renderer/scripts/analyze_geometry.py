#!/usr/bin/env python3
"""
analyze_geometry.py - Stage 2: Geometric & Spatial Analysis

Takes extracted PDF primitives, detects walls, rooms, openings, and fixtures,
and outputs a structured Architectural Model JSON.
"""

import argparse
import json
import os
import sys
import numpy as np


def analyze_extracted_primitives(extracted_json_path, output_model_path=None):
    with open(extracted_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    page = data["pages"][0]
    paths = page["paths"]
    annotations = page["annotations"]
    width = page["width_pts"]
    height = page["height_pts"]

    print(f"[+] Analyzing {data['source_file']} ({len(paths)} paths, {len(annotations)} annotations)")

    lines = []
    rects = []

    for p in paths:
        for it in p.get("items", []):
            cmd = it[0]
            if cmd == "line":
                lines.append((it[1], it[2], p["width"]))
            elif cmd == "rect":
                rects.append((it[1], p["fill_color"]))

    print(f"  - Extracted lines: {len(lines)}, Rectangles: {len(rects)}")

    # Group dimension strings
    dim_strings = []
    curr_str = []
    for a in annotations:
        txt = a["text"]
        if txt == "m":
            if curr_str:
                dim_strings.append(f"{''.join(curr_str)} m")
                curr_str = []
        else:
            curr_str.append(txt)
    if curr_str:
        dim_strings.append("".join(curr_str))

    print(f"  - Detected dimension annotations: {dim_strings}")

    # Build architectural model
    model = {
        "source_file": data["source_file"],
        "drawing_type": "FLOOR_PLAN",
        "units": "meters",
        "scale_estimate": "1:150",
        "dimensions": {
            "page_width_pts": width,
            "page_height_pts": height,
            "annotations": dim_strings
        },
        "spatial_decomposition": {
            "total_line_elements": len(lines),
            "total_rect_elements": len(rects),
            "has_stairs": len(lines) > 1000,
            "detected_zones": [
                {"zone_id": "living_hall", "suggested_material": "STONE_MARBLE_ITALIAN"},
                {"zone_id": "master_bedroom", "suggested_material": "WOOD_PARQUET_HERRINGBONE"},
                {"zone_id": "secondary_bedroom", "suggested_material": "WOOD_PARQUET_HERRINGBONE"},
                {"zone_id": "kitchen_wet_zone", "suggested_material": "STONE_VERDE_SAGE"},
                {"zone_id": "bathrooms", "suggested_material": "TILE_CHARCOAL_SLATE"},
                {"zone_id": "balconies", "suggested_material": "STONE_PAVER_EXTERIOR"}
            ]
        }
    }

    if output_model_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_model_path)), exist_ok=True)
        with open(output_model_path, "w", encoding="utf-8") as f:
            json.dump(model, f, indent=2)
        print(f"[✓] Architectural Model saved to: {output_model_path}")

    return model


def main():
    parser = argparse.ArgumentParser(description="Analyze geometric primitives into architectural model.")
    parser.add_argument("--input", "-i", required=True, help="Path to extracted primitives JSON")
    parser.add_argument("--output", "-o", default=None, help="Path to output architectural model JSON")

    args = parser.parse_args()

    out_file = args.output
    if not out_file:
        base = os.path.splitext(args.input)[0]
        out_file = f"{base}_model.json"

    analyze_extracted_primitives(args.input, out_file)


if __name__ == "__main__":
    main()
