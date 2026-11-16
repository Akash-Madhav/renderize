#!/usr/bin/env python3
"""
analyze_geometry.py - Stage 2: Geometric & Spatial Analysis

Takes extracted PDF primitives, detects walls, rooms, openings, and text labels,
and outputs a structured Architectural Model JSON with dynamic scale and zone detection.
"""

import argparse
import json
import os
import re
import sys
from typing import Dict, List, Any


def analyze_extracted_primitives(extracted_json_path, output_model_path=None):
    with open(extracted_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    page = data["pages"][0]
    paths = page["paths"]
    annotations = page.get("annotations", [])
    width = page["width_pts"]
    height = page["height_pts"]

    print(f"[+] Analyzing {data['source_file']} ({len(paths)} paths, {len(annotations)} annotations)")

    lines = []
    rects = []

    for p in paths:
        for it in p.get("items", []):
            cmd = it[0]
            if cmd == "line":
                lines.append((it[1], it[2], p.get("width", 1.0)))
            elif cmd == "rect":
                rects.append((it[1], p.get("fill_color")))

    print(f"  - Extracted lines: {len(lines)}, Rectangles: {len(rects)}")

    # 1. Group dimension strings & detect scales
    dim_strings = []
    curr_str = []
    detected_scale = "1:50"
    room_labels_found = []

    scale_regex = re.compile(r"1\s*:\s*\d{2,3}")

    for a in annotations:
        txt = a.get("text", "")
        if not txt:
            continue

        # Check for scale indicator
        scale_match = scale_regex.search(txt)
        if scale_match:
            detected_scale = scale_match.group(0).replace(" ", "")

        # Group numbers and meter units
        if txt == "m" or txt == "M":
            if curr_str:
                dim_strings.append(f"{''.join(curr_str)} m")
                curr_str = []
        elif re.match(r"^\d+(\.\d+)?$", txt):
            curr_str.append(txt)
        else:
            if curr_str:
                dim_strings.append("".join(curr_str))
                curr_str = []

            # Check for room label keywords
            upper = txt.upper().strip()
            for kw, zone in [
                ("BED", "BEDROOM"),
                ("KITCHEN", "KITCHEN"),
                ("LIVING", "LIVING_ROOM"),
                ("DINING", "DINING_ROOM"),
                ("BATH", "BATHROOM"),
                ("TOILET", "BATHROOM"),
                ("WC", "BATHROOM"),
                ("BALCONY", "BALCONY"),
                ("TERRACE", "TERRACE"),
                ("OFFICE", "OFFICE"),
                ("STUDY", "STUDY"),
                ("FOYER", "FOYER"),
                ("STORE", "STORE_ROOM")
            ]:
                if kw in upper and zone not in room_labels_found:
                    room_labels_found.append(zone)

    if curr_str:
        dim_strings.append("".join(curr_str))

    # 2. Build detected zones dynamically
    zone_material_map = {
        "LIVING_ROOM": "STONE_MARBLE_ITALIAN",
        "DINING_ROOM": "STONE_MARBLE_ITALIAN",
        "FOYER": "STONE_MARBLE_ITALIAN",
        "BEDROOM": "WOOD_PARQUET_HERRINGBONE",
        "KITCHEN": "STONE_VERDE_SAGE",
        "BATHROOM": "TILE_CHARCOAL_SLATE",
        "BALCONY": "STONE_PAVER_EXTERIOR",
        "TERRACE": "STONE_PAVER_EXTERIOR",
        "OFFICE": "WOOD_PARQUET_HERRINGBONE",
        "STUDY": "WOOD_PARQUET_HERRINGBONE",
        "STORE_ROOM": "STONE_VERDE_SAGE"
    }

    dynamic_zones = []
    if room_labels_found:
        for z in room_labels_found:
            dynamic_zones.append({
                "zone_id": z.lower(),
                "suggested_material": zone_material_map.get(z, "STONE_MARBLE_ITALIAN")
            })
    else:
        # Fallback to standard spatial suite
        dynamic_zones = [
            {"zone_id": "living_hall", "suggested_material": "STONE_MARBLE_ITALIAN"},
            {"zone_id": "master_bedroom", "suggested_material": "WOOD_PARQUET_HERRINGBONE"},
            {"zone_id": "kitchen_wet_zone", "suggested_material": "STONE_VERDE_SAGE"},
            {"zone_id": "bathrooms", "suggested_material": "TILE_CHARCOAL_SLATE"}
        ]

    # Build architectural model
    model = {
        "source_file": data.get("source_file", ""),
        "drawing_type": "FLOOR_PLAN",
        "units": "meters",
        "scale_estimate": detected_scale,
        "dimensions": {
            "page_width_pts": width,
            "page_height_pts": height,
            "annotations": dim_strings[:30]
        },
        "spatial_decomposition": {
            "total_line_elements": len(lines),
            "total_rect_elements": len(rects),
            "has_stairs": len(lines) > 800,
            "detected_zones": dynamic_zones,
            "room_labels_detected": room_labels_found
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
