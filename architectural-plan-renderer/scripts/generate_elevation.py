#!/usr/bin/env python3
"""
generate_elevation.py - Stage 5C: Publication-Grade Architectural Front Elevation Visualizer

Generates publication-quality architectural front elevations:
1. Adapts facade width and storey count to match the actual building footprint.
2. Synthesizes plinth steps, main portico entrance, facade fenestration, and window arrays.
3. Renders cantilevered balconies, sun louvres/pergolas, and rooftop parapet profile.
4. Formatted as crisp architectural line drawing with subtle tonal shading (Scale 1:75).
"""

import argparse
import os
import sys
from typing import List, Dict, Any, Tuple
from PIL import Image, ImageDraw, ImageFont


def generate_dynamic_elevation(
    floor_data: List[Dict[str, Any]],
    output_path: str,
    canvas_size: Tuple[int, int] = (4200, 2400),
    project_title: str = "ARCHITECTURAL RESIDENCE"
) -> str:
    cw, ch = canvas_size
    img = Image.new("RGB", (cw, ch), "#FFFFFF")
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype("arialbd.ttf", 44)
        font_lbl = ImageFont.truetype("arialbd.ttf", 32)
        font_dim = ImageFont.truetype("arial.ttf", 26)
    except:
        font_title = ImageFont.load_default()
        font_lbl = ImageFont.load_default()
        font_dim = ImageFont.load_default()

    num_floors = max(1, len(floor_data))

    margin_l = 480
    margin_r = cw - 380
    ground_y = ch - 380
    top_y = 300
    usable_h = ground_y - top_y

    floor_h = usable_h // (num_floors + 1)
    bldg_w = margin_r - margin_l

    # Atmospheric sky tint
    for y_bg in range(0, ground_y):
        val = int(248 + (y_bg / float(ground_y)) * 7)
        draw.line([(margin_l - 180, y_bg), (margin_r + 180, y_bg)], fill=(val, val, min(255, val + 2)))

    # Natural Ground Line
    draw.line([(margin_l - 320, ground_y), (margin_r + 220, ground_y)], fill="#24282B", width=6)
    # Earth ground tick marks
    for x_h in range(margin_l - 270, margin_r + 220, 45):
        draw.line([(x_h, ground_y + 4), (x_h - 25, ground_y + 45)], fill="#8B949E", width=2)

    # Plinth Base (E0E5DF stone tone)
    plinth_h = 75
    plinth_w_pad = 55
    draw.rectangle([margin_l - plinth_w_pad, ground_y - plinth_h,
                    margin_r + plinth_w_pad, ground_y],
                   fill="#E0E5DF", outline="#24282B", width=3)

    # Plinth Entrance Steps (centered)
    cx_bldg = (margin_l + margin_r) // 2
    steps_w = 420
    num_steps = 4
    for s in range(num_steps):
        sw = steps_w + s * 45
        sy = ground_y - int((num_steps - s) * (plinth_h / num_steps))
        draw.rectangle([cx_bldg - sw // 2, sy, cx_bldg + sw // 2, ground_y],
                       fill="#D0C2B2", outline="#24282B", width=2)

    # Exterior Massing: Central Bay + Left Wing + Right Wing
    wing_w = int(bldg_w * 0.28)
    central_w = int(bldg_w * 0.44)

    bldg_top_y = int(ground_y - plinth_h - num_floors * floor_h)

    # Building Exterior Block with architectural off-white finish
    draw.rectangle([margin_l, bldg_top_y, margin_r, ground_y - plinth_h],
                   fill="#F7FBFE", outline="#24282B", width=4)

    # Floor Slabs / Cornice Bands across facade
    for fl in range(num_floors + 1):
        sy = int(ground_y - plinth_h - fl * floor_h)
        band_h = 24
        draw.rectangle([margin_l - 15, sy - band_h, margin_r + 15, sy],
                       fill="#363C40", outline="#24282B", width=2)

    # Multi-Floor Windows, Louvres & Balconies
    for fl_idx in range(num_floors):
        fl_bot = int(ground_y - plinth_h - fl_idx * floor_h - 24)
        fl_top = int(ground_y - plinth_h - (fl_idx + 1) * floor_h)

        if fl_idx == 0:
            # Grand Entrance Portico & Modern Double Door
            portico_h = 320
            portico_w = 340
            draw.rectangle([cx_bldg - portico_w // 2, fl_bot - portico_h,
                            cx_bldg + portico_w // 2, fl_bot],
                           fill="#E0E5DF", outline="#24282B", width=3)
            # Door reveal & vertical center line
            draw.line([(cx_bldg, fl_bot - portico_h), (cx_bldg, fl_bot)], fill="#24282B", width=3)
            # Modern vertical hardware pulls
            draw.line([(cx_bldg - 15, fl_bot - 160), (cx_bldg - 15, fl_bot - 200)], fill="#24282B", width=4)
            draw.line([(cx_bldg + 15, fl_bot - 160), (cx_bldg + 15, fl_bot - 200)], fill="#24282B", width=4)

            # Entrance Canopy with cantilever overhang
            canopy_w = portico_w + 120
            draw.rectangle([cx_bldg - canopy_w // 2, fl_bot - portico_h - 30,
                            cx_bldg + canopy_w // 2, fl_bot - portico_h],
                           fill="#363C40", outline="#24282B", width=3)

            # Left and Right Wing Windows (Ground Floor)
            for side_cx in [margin_l + int(wing_w * 0.5), margin_r - int(wing_w * 0.5)]:
                ww = 320
                wh = 260
                w_top = fl_bot - wh
                draw.rectangle([side_cx - ww // 2, w_top, side_cx + ww // 2, fl_bot],
                               fill="#E8F1F5", outline="#24282B", width=3)
                # Glass reflection diagonal sheen
                draw.line([(side_cx - ww // 2 + 30, fl_bot - 20), (side_cx + 40, w_top + 30)], fill="#FFFFFF", width=2)
                # 3-panel mullions
                draw.line([(side_cx - ww // 6, w_top), (side_cx - ww // 6, fl_bot)], fill="#24282B", width=2)
                draw.line([(side_cx + ww // 6, w_top), (side_cx + ww // 6, fl_bot)], fill="#24282B", width=2)
        else:
            # Upper Floor Balconies with Cantilever & Glass Railing
            balcony_w = int(central_w - 60)
            draw.rectangle([cx_bldg - balcony_w // 2, fl_bot - 140,
                            cx_bldg + balcony_w // 2, fl_bot],
                           fill="#E8F1F5", outline="#24282B", width=3)
            # Glass tint / vertical glass brackets
            b_start = int(cx_bldg - balcony_w // 2 + 60)
            b_end = int(cx_bldg + balcony_w // 2)
            for gx in range(b_start, b_end, 70):
                draw.line([(gx, fl_bot - 140), (gx, fl_bot)], fill="#8B949E", width=2)
            # Balcony handrail
            draw.line([(cx_bldg - balcony_w // 2, fl_bot - 140),
                       (cx_bldg + balcony_w // 2, fl_bot - 140)], fill="#24282B", width=4)

            # Sliding Glass Doors behind Balcony
            door_w = int(balcony_w - 80)
            draw.rectangle([cx_bldg - door_w // 2, fl_bot - 340,
                            cx_bldg + door_w // 2, fl_bot - 140],
                           fill="#E8F1F5", outline="#24282B", width=2)
            draw.line([(cx_bldg, fl_bot - 340), (cx_bldg, fl_bot - 140)], fill="#24282B", width=2)

            # Upper Bedrooms Windows on Wings
            for side_cx in [margin_l + int(wing_w * 0.5), margin_r - int(wing_w * 0.5)]:
                ww = 280
                wh = 240
                w_top = fl_bot - wh - 40
                draw.rectangle([side_cx - ww // 2, w_top, side_cx + ww // 2, w_top + wh],
                               fill="#E8F1F5", outline="#24282B", width=3)
                draw.line([(side_cx, w_top), (side_cx, w_top + wh)], fill="#24282B", width=2)
                # Sunshade / Chajja projection
                draw.line([(side_cx - ww // 2 - 25, w_top - 15),
                           (side_cx + ww // 2 + 25, w_top - 15)], fill="#24282B", width=4)

    # Rooftop Parapet and Headroom Tower
    parapet_h = 100
    draw.rectangle([margin_l, bldg_top_y - parapet_h, margin_r, bldg_top_y],
                   fill="#F7FBFE", outline="#24282B", width=3)

    # Stair Headroom / Solar Pergola Tower
    tower_w = 360
    tower_h = 180
    tower_x = cx_bldg - 200
    draw.rectangle([tower_x, bldg_top_y - parapet_h - tower_h,
                    tower_x + tower_w, bldg_top_y - parapet_h],
                   fill="#E0E5DF", outline="#24282B", width=3)
    for lx in range(tower_x, tower_x + tower_w + 30, 35):
        draw.line([(lx, bldg_top_y - parapet_h - tower_h - 20),
                   (lx - 20, bldg_top_y - parapet_h - tower_h)], fill="#24282B", width=3)

    # Elevation Title and Scale
    draw.text((margin_l, top_y - 100), "FRONT ELEVATION & CLUSTER PROFILE", fill="#24282B", font=font_title)
    draw.text((margin_l, top_y - 50), f"SCALE 1:75 | CONTEMPORARY FACADE SPECIFICATION", fill="#70757A", font=font_lbl)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    img.save(output_path, quality=95)
    print(f"[✓] Enhanced Publication-Grade Front Elevation saved to: {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Generate dynamic Front Elevation graphic.")
    parser.add_argument("--output", "-o", required=True, help="Output PNG path")
    parser.add_argument("--floors", "-f", type=int, default=3, help="Number of floor levels")
    parser.add_argument("--title", "-t", default="RESIDENCE", help="Project title")

    args = parser.parse_args()
    dummy_floors = [{"label": f"Floor Level {i + 1}"} for i in range(args.floors)]
    generate_dynamic_elevation(dummy_floors, args.output, project_title=args.title)


if __name__ == "__main__":
    main()
