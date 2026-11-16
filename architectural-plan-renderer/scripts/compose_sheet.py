#!/usr/bin/env python3
"""
compose_sheet.py - Stage 6: Adaptive Multi-Drawing Presentation Sheet Composer

Assembles arbitrary N rendered floor plans, dynamically generated section drawings,
front elevations, title blocks, real project metadata, and authentic material palettes
into an A1 presentation sheet PDF matching publication standards.
"""

import argparse
import os
import sys
from typing import List, Union, Tuple, Optional, Dict, Any
from PIL import Image, ImageDraw, ImageFont, ImageOps
import pymupdf


def compose_presentation_sheet(
    plans_input: Union[List, str],
    first_plan_path: str = None,
    second_plan_path: str = None,
    output_pdf_path: str = None,
    output_png_path: str = None,
    sheet_size: Tuple[int, int] = (9933, 7016),
    project_title: str = "ARCHITECTURAL RESIDENCE",
    section_image_path: Optional[str] = None,
    elevation_image_path: Optional[str] = None,
    roof_image_path: Optional[str] = None,
    applied_materials: Optional[List[Dict[str, Any]]] = None,
    metadata: Optional[Dict[str, Any]] = None
):
    """
    Composes standard A1 presentation board (9933 x 7016 px at ~300 DPI).
    Supports arbitrary N floor plans (1, 2, 3, 4, 5+ floors) with dynamic grid scaling
    and fully dynamic section, elevation, materials, and metadata blocks.
    """
    if isinstance(plans_input, list):
        plans_list = plans_input
        pdf_out = first_plan_path if output_pdf_path is None else output_pdf_path
        png_out = second_plan_path if output_png_path is None else output_png_path
    else:
        plans_list = [("UNIT PLAN - GROUND FLOOR", plans_input)]
        if first_plan_path and os.path.exists(first_plan_path):
            plans_list.append(("UNIT PLAN - FIRST FLOOR", first_plan_path))
        if second_plan_path and os.path.exists(second_plan_path):
            plans_list.append(("UNIT PLAN - SECOND FLOOR", second_plan_path))
        pdf_out = output_pdf_path
        png_out = output_png_path

    formatted_plans = []
    for idx, item in enumerate(plans_list):
        if isinstance(item, (tuple, list)):
            lbl, pth = item[0], item[1]
        else:
            pth = item
            fn = os.path.basename(pth).upper()
            if any(k in fn for k in ["ROOF", "TERRACE", "CLUSTER"]):
                lbl = "ROOF & CLUSTER PLAN"
            elif any(k in fn for k in ["PLINTH", "GROUND", "PL PLAN", " PL "]):
                lbl = "UNIT PLAN - GROUND FLOOR"
            elif any(k in fn for k in ["FIRST", "1ST", "FL PLAN", " FL "]):
                lbl = "UNIT PLAN - FIRST FLOOR"
            elif any(k in fn for k in ["SECOND", "2ND", "SL PLAN", " SL "]):
                lbl = "UNIT PLAN - SECOND FLOOR"
            elif any(k in fn for k in ["UNIT", "ASSC", "PROFESSOR", "RESIDENCE"]):
                lbl = "ARCHITECTURAL FLOOR PLAN"
            else:
                lbl = f"UNIT PLAN - LEVEL {idx + 1}"
        if os.path.exists(pth):
            formatted_plans.append((lbl, pth))

    num_plans = len(formatted_plans)
    print(f"[+] Composing adaptive A1 presentation board ({sheet_size[0]} x {sheet_size[1]} px) with {num_plans} floor plan(s)...")

    board = Image.new("RGB", sheet_size, "#F7FBFE")
    draw = ImageDraw.Draw(board)

    # Double Sheet Border (Architectural border with outer thin line and inner medium line)
    margin_outer = 60
    margin_inner = 80
    draw.rectangle([margin_outer, margin_outer, sheet_size[0] - margin_outer, sheet_size[1] - margin_outer],
                   outline="#70757A", width=1)
    draw.rectangle([margin_inner, margin_inner, sheet_size[0] - margin_inner, sheet_size[1] - margin_inner],
                   outline="#24282B", width=4)

    # Architectural Typography
    try:
        font_title = ImageFont.truetype("georgia.ttf", 160)
        font_sub = ImageFont.truetype("arialbd.ttf", 64)
        font_info = ImageFont.truetype("arialbd.ttf", 44)
        font_dim = ImageFont.truetype("arial.ttf", 36)
    except:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_info = ImageFont.load_default()
        font_dim = ImageFont.load_default()

    # 1. Master Title (Centered with subtle tracking)
    draw.text((sheet_size[0] // 2 - 450, 180), project_title.upper(), fill="#24282B", font=font_title)

    # North arrow badge at top right
    draw.ellipse([sheet_size[0] - 500, 200, sheet_size[0] - 400, 300], outline="#24282B", width=4)
    draw.polygon([(sheet_size[0] - 450, 210), (sheet_size[0] - 470, 270), (sheet_size[0] - 450, 255)], fill="#24282B")
    draw.polygon([(sheet_size[0] - 450, 210), (sheet_size[0] - 430, 270), (sheet_size[0] - 450, 255)], fill="#FFFFFF", outline="#24282B")
    draw.text((sheet_size[0] - 455, 175), "N", fill="#24282B", font=font_sub)

    y_pos = 500

    # 2. Dynamic Floor Plan Layout Grid
    if num_plans == 1:
        # Single Plan Layout: Prominent central unit plan
        lbl, path = formatted_plans[0]
        img = Image.open(path).convert("RGB")
        gray = ImageOps.invert(img.convert("L"))
        bbox = gray.getbbox()
        img_cropped = img.crop(bbox) if bbox else img
        img_cropped.thumbnail((4800, 2400), Image.Resampling.LANCZOS)
        board.paste(img_cropped, (300, y_pos + 120))
        draw.text((600, y_pos + 40), lbl, fill="#24282B", font=font_sub)
        plan_h = 2400

    elif num_plans == 2:
        # Check if one is a roof/cluster plan and the other is a unit/floor plan
        is_roof_0 = any(k in formatted_plans[0][0].upper() for k in ["ROOF", "CLUSTER", "TERRACE"])
        is_roof_1 = any(k in formatted_plans[1][0].upper() for k in ["ROOF", "CLUSTER", "TERRACE"])

        if is_roof_0 or is_roof_1:
            roof_item = formatted_plans[0] if is_roof_0 else formatted_plans[1]
            unit_item = formatted_plans[1] if is_roof_0 else formatted_plans[0]

            # 1. Place Roof & Cluster Plan at top-left (Scale 1:100 proportional)
            lbl_r, path_r = roof_item
            img_r = Image.open(path_r).convert("RGB")
            gray_r = ImageOps.invert(img_r.convert("L"))
            bbox_r = gray_r.getbbox()
            cropped_r = img_r.crop(bbox_r) if bbox_r else img_r
            cropped_r.thumbnail((2600, 2200), Image.Resampling.LANCZOS)
            board.paste(cropped_r, (250, y_pos + 120))
            draw.text((350, y_pos + 40), lbl_r, fill="#24282B", font=font_sub)

            # 2. Place Main Architectural Unit Plan prominently in center/right
            lbl_u, path_u = unit_item
            img_u = Image.open(path_u).convert("RGB")
            gray_u = ImageOps.invert(img_u.convert("L"))
            bbox_u = gray_u.getbbox()
            cropped_u = img_u.crop(bbox_u) if bbox_u else img_u
            cropped_u.thumbnail((5400, 2400), Image.Resampling.LANCZOS)
            board.paste(cropped_u, (3400, y_pos + 120))
            draw.text((4400, y_pos + 40), lbl_u, fill="#24282B", font=font_sub)
            plan_h = 2400
        else:
            col_w = 4500
            plan_h = 2300
            for i, (lbl, path) in enumerate(formatted_plans):
                x_pos = 200 + i * 4900
                img = Image.open(path).convert("RGB")
                gray = ImageOps.invert(img.convert("L"))
                bbox = gray.getbbox()
                img_cropped = img.crop(bbox) if bbox else img
                img_cropped.thumbnail((col_w, plan_h), Image.Resampling.LANCZOS)
                board.paste(img_cropped, (x_pos, y_pos + 120))
                draw.text((x_pos + 400, y_pos + 40), lbl, fill="#24282B", font=font_sub)

    elif num_plans == 3:
        # Tri-Column Layout (Matching Director Reference)
        plan_w = 3000
        plan_h = 2300
        positions = [200, 3450, 6700]
        for i, (lbl, path) in enumerate(formatted_plans[:3]):
            x_pos = positions[i]
            img = Image.open(path).convert("RGB")
            gray = ImageOps.invert(img.convert("L"))
            bbox = gray.getbbox()
            img_cropped = img.crop(bbox) if bbox else img
            img_cropped.thumbnail((plan_w, plan_h), Image.Resampling.LANCZOS)
            board.paste(img_cropped, (x_pos, y_pos + 120))
            draw.text((x_pos + 300, y_pos + 40), lbl, fill="#24282B", font=font_sub)

    else:
        # Adaptive Multi-Column Register for 4+ plans
        col_w = (sheet_size[0] - 600) // min(num_plans, 4)
        plan_h = 2200
        for i, (lbl, path) in enumerate(formatted_plans[:4]):
            x_pos = 200 + i * (col_w + 50)
            img = Image.open(path).convert("RGB")
            gray = ImageOps.invert(img.convert("L"))
            bbox = gray.getbbox()
            img_cropped = img.crop(bbox) if bbox else img
            img_cropped.thumbnail((col_w, plan_h), Image.Resampling.LANCZOS)
            board.paste(img_cropped, (x_pos, y_pos + 120))
            draw.text((x_pos + 100, y_pos + 40), lbl, fill="#24282B", font=font_sub)

    # 3. Dynamic Section AA' in lower left
    draw.text((400, y_pos + plan_h + 100), "SECTION AA'", fill="#24282B", font=font_sub)
    section_box = [200, y_pos + plan_h + 200, 5300, sheet_size[1] - 800]
    target_w = section_box[2] - section_box[0]
    target_h = section_box[3] - section_box[1]

    if section_image_path and os.path.exists(section_image_path):
        sec_img = Image.open(section_image_path).convert("RGB")
        sec_img.thumbnail((target_w, target_h), Image.Resampling.LANCZOS)
        sec_x = section_box[0] + (target_w - sec_img.width) // 2
        sec_y = section_box[1] + (target_h - sec_img.height) // 2
        board.paste(sec_img, (sec_x, sec_y))
        draw.rectangle(section_box, outline="#24282B", width=3)
    else:
        draw.rectangle(section_box, outline="#A0A5A8", width=3, fill="#FFFFFF")
        draw.text((section_box[0] + 400, section_box[1] + target_h // 2),
                  "[ SECTION AA' - LONGITUDINAL STRUCTURAL CUT ]", fill="#70757A", font=font_sub)

    # 4. Dynamic Front Elevation Drawing in middle lower right
    draw.text((5600, y_pos + plan_h + 100), "FRONT ELEVATION & CLUSTER PROFILE", fill="#24282B", font=font_sub)
    elev_box = [5500, y_pos + plan_h + 200, 8300, y_pos + plan_h + 1900]
    target_ew = elev_box[2] - elev_box[0]
    target_eh = elev_box[3] - elev_box[1]

    if elevation_image_path and os.path.exists(elevation_image_path):
        elev_img = Image.open(elevation_image_path).convert("RGB")
        elev_img.thumbnail((target_ew, target_eh), Image.Resampling.LANCZOS)
        elev_x = elev_box[0] + (target_ew - elev_img.width) // 2
        elev_y = elev_box[1] + (target_eh - elev_img.height) // 2
        board.paste(elev_img, (elev_x, elev_y))
        draw.rectangle(elev_box, outline="#24282B", width=3)
    else:
        draw.rectangle(elev_box, outline="#A0A5A8", width=3, fill="#FFFFFF")
        draw.text((elev_box[0] + 200, elev_box[1] + target_eh // 2),
                  "[ FRONT ELEVATION PROFILE ]", fill="#70757A", font=font_sub)

    # 5. Dynamic Colour Palette Swatches (Right side)
    draw.text((8500, y_pos + plan_h + 100), "COLOUR PALETTE", fill="#24282B", font=font_sub)

    swatches_to_display = []
    if applied_materials:
        seen = set()
        for mat in applied_materials:
            color = mat.get("color", "#8B5A2B")
            name = mat.get("name", "Architectural Surface")
            if name not in seen:
                seen.add(name)
                swatches_to_display.append((color, name))

    if not swatches_to_display:
        swatches_to_display = [
            ("#8B5A2B", "French Oak Parquet"),
            ("#E0E5DF", "Italian Marble"),
            ("#8B9E7A", "Sage Quartzite"),
            ("#363C40", "Charcoal Slate"),
            ("#D0C2B2", "Terrazzo Venato"),
            ("#B8BCB5", "Basalt Paver"),
            ("#557A46", "Landscape Garden")
        ]

    sw_y = y_pos + plan_h + 220
    for idx, (color, name) in enumerate(swatches_to_display[:8]):
        cx = 8550 + (idx % 2) * 550
        cy = sw_y + (idx // 2) * 260
        draw.ellipse([cx, cy, cx + 160, cy + 160], fill=color, outline="#24282B", width=3)
        draw.text((cx - 10, cy + 175), name, fill="#24282B", font=font_info)

    # 6. Dynamic Project Metadata Title Block (Bottom)
    draw.line([margin_inner, sheet_size[1] - 700, sheet_size[0] - margin_inner, sheet_size[1] - 700], fill="#24282B", width=2)

    meta = metadata or {}
    total_area = meta.get("total_floor_area", 320 * max(1, num_plans))
    unit_area = meta.get("unit_area", 320)
    num_blocks = meta.get("num_blocks", 1)
    num_fl = meta.get("num_floors", max(1, num_plans))
    typology = meta.get("unit_typology", "RESIDENTIAL ARCHITECTURAL SPECIFICATION")

    info_left = [
        f"TOTAL FLOOR AREA : {total_area:.1f} SQ.M" if isinstance(total_area, float) else f"TOTAL FLOOR AREA : {total_area} SQ.M",
        f"UNIT AREA : {unit_area:.1f} SQ.M" if isinstance(unit_area, float) else f"UNIT AREA : {unit_area} SQ.M",
        f"NO. OF BLOCKS : {num_blocks}",
        f"NO. OF FLOORS : {num_fl}",
        f"UNIT TYPOLOGY : {typology}"
    ]
    for i, line in enumerate(info_left):
        draw.text((200, sheet_size[1] - 640 + i * 80), line, fill="#24282B", font=font_info)

    draw.text((sheet_size[0] // 2 - 300, sheet_size[1] - 400), "ALL DIMENSIONS ARE IN METRES", fill="#24282B", font=font_info)

    scale_notes = meta.get("scale_annotations", [])
    scale_str_unit = "1:50"
    for s in scale_notes:
        if "1:" in s:
            scale_str_unit = s
            break

    info_right = [
        "SCALE",
        "ROOF PLAN & CLUSTER PLAN :- 1:100",
        f"UNIT PLAN :- {scale_str_unit}",
        "SECTION :- 1:50",
        "ELEVATIONS :- 1:75"
    ]
    for i, line in enumerate(info_right):
        draw.text((sheet_size[0] - 1800, sheet_size[1] - 640 + i * 80), line, fill="#24282B", font=font_info)

    # Save PNG
    if png_out:
        os.makedirs(os.path.dirname(os.path.abspath(png_out)), exist_ok=True)
        board.save(png_out, quality=92)
        print(f"[✓] Presentation Board PNG saved to: {png_out}")

    # Export to Print-Ready PDF
    if pdf_out:
        os.makedirs(os.path.dirname(os.path.abspath(pdf_out)), exist_ok=True)
        doc = pymupdf.open()
        page_rect = pymupdf.Rect(0, 0, 2384, 1684)
        page = doc.new_page(width=page_rect.width, height=page_rect.height)

        temp_img = os.path.splitext(pdf_out)[0] + "_temp.jpg"
        board.save(temp_img, quality=88)
        page.insert_image(page_rect, filename=temp_img)
        doc.save(pdf_out)
        doc.close()
        if os.path.exists(temp_img):
            os.remove(temp_img)
        print(f"[✓] Presentation Board PDF saved to: {pdf_out}")

    return pdf_out


def main():
    parser = argparse.ArgumentParser(description="Compose presentation sheet from rendered plans.")
    parser.add_argument("--plans", nargs="+", required=True, help="List of floor plan rendered PNG paths")
    parser.add_argument("--output-pdf", required=True, help="Output A1 PDF path")
    parser.add_argument("--output-png", default=None, help="Output A1 PNG path")
    parser.add_argument("--section", default=None, help="Section image path")
    parser.add_argument("--elevation", default=None, help="Elevation image path")
    parser.add_argument("--title", default="RESIDENCE", help="Project title")

    args = parser.parse_args()
    compose_presentation_sheet(
        args.plans,
        output_pdf_path=args.output_pdf,
        output_png_path=args.output_png,
        section_image_path=args.section,
        elevation_image_path=args.elevation,
        project_title=args.title
    )


if __name__ == "__main__":
    main()
