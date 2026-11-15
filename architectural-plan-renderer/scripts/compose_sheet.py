#!/usr/bin/env python3
"""
compose_sheet.py - Stage 6: Adaptive Multi-Drawing Presentation Sheet Composer

Assembles arbitrary N rendered floor plans, section drawings, front elevations,
title blocks, project metadata, and scale information into an A1 presentation sheet PDF
matching the reference layout of DIRECTOR SHEET 1.pdf.
"""

import argparse
import os
import sys
from typing import List, Union, Tuple
from PIL import Image, ImageDraw, ImageFont, ImageOps
import pymupdf


def compose_presentation_sheet(plans_input: Union[List, str],
                               first_plan_path: str = None,
                               second_plan_path: str = None,
                               output_pdf_path: str = None,
                               output_png_path: str = None,
                               sheet_size: Tuple[int, int] = (9933, 7016),
                               project_title: str = "DIRECTOR"):
    """
    Composes standard A1 presentation board (9933 x 7016 px at ~300 DPI).
    Supports arbitrary N floor plans (1, 2, 3, 4, 5+ floors) with dynamic grid scaling.
    """
    # Normalize input: can be a list of paths or 3 discrete paths for backwards compatibility
    if isinstance(plans_input, list):
        plans_list = plans_input
        pdf_out = first_plan_path if output_pdf_path is None else output_pdf_path
        png_out = second_plan_path if output_png_path is None else output_png_path
    else:
        # Legacy positional invocation
        plans_list = [
            ("UNIT PLAN - GROUND FLOOR", plans_input),
        ]
        if first_plan_path and os.path.exists(first_plan_path):
            plans_list.append(("UNIT PLAN - FIRST FLOOR", first_plan_path))
        if second_plan_path and os.path.exists(second_plan_path):
            plans_list.append(("UNIT PLAN - SECOND FLOOR", second_plan_path))
        pdf_out = output_pdf_path
        png_out = output_png_path

    # Ensure plans_list is formatted as [(label, path), ...]
    formatted_plans = []
    for idx, item in enumerate(plans_list):
        if isinstance(item, tuple) or isinstance(item, list):
            lbl, pth = item[0], item[1]
        else:
            pth = item
            fn = os.path.basename(pth).upper()
            if any(k in fn for k in ["PLINTH", "GROUND", "PL PLAN", " PL "]):
                lbl = "UNIT PLAN - GROUND FLOOR"
            elif any(k in fn for k in ["FIRST", "1ST", "FL PLAN", " FL "]):
                lbl = "UNIT PLAN - FIRST FLOOR"
            elif any(k in fn for k in ["SECOND", "2ND", "SL PLAN", " SL "]):
                lbl = "UNIT PLAN - SECOND FLOOR"
            elif any(k in fn for k in ["ROOF", "TERRACE"]):
                lbl = "ROOF & CLUSTER PLAN"
            else:
                lbl = f"UNIT PLAN - LEVEL {idx + 1}"
        if os.path.exists(pth):
            formatted_plans.append((lbl, pth))

    num_plans = len(formatted_plans)
    print(f"[+] Composing adaptive A1 presentation board ({sheet_size[0]} x {sheet_size[1]} px) with {num_plans} floor plan(s)...")

    board = Image.new("RGB", sheet_size, "#F7FBFE")
    draw = ImageDraw.Draw(board)

    # Sheet Border
    margin = 80
    draw.rectangle([margin, margin, sheet_size[0] - margin, sheet_size[1] - margin], outline="#24282B", width=4)

    # Fonts
    try:
        font_title = ImageFont.truetype("georgia.ttf", 160)
        font_sub = ImageFont.truetype("arialbd.ttf", 64)
        font_info = ImageFont.truetype("arialbd.ttf", 44)
    except:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_info = ImageFont.load_default()

    # 1. Master Title
    draw.text((sheet_size[0] // 2 - 400, 180), project_title, fill="#24282B", font=font_title)

    # North arrow badge at top right
    draw.ellipse([sheet_size[0] - 500, 200, sheet_size[0] - 400, 300], outline="#24282B", width=4)
    draw.polygon([(sheet_size[0] - 450, 210), (sheet_size[0] - 470, 270), (sheet_size[0] - 450, 255)], fill="#24282B")
    draw.polygon([(sheet_size[0] - 450, 210), (sheet_size[0] - 430, 270), (sheet_size[0] - 450, 255)], fill="#FFFFFF", outline="#24282B")
    draw.text((sheet_size[0] - 455, 175), "N", fill="#24282B", font=font_sub)

    y_pos = 500

    # 2. Dynamic Floor Plan Layout
    if num_plans == 1:
        # Single Plan Layout: Prominent central unit plan
        lbl, path = formatted_plans[0]
        img = Image.open(path).convert("RGB")
        # Crop whitespace to tightly focus on plan
        gray = ImageOps.invert(img.convert("L"))
        bbox = gray.getbbox()
        img_cropped = img.crop(bbox) if bbox else img
        img_cropped.thumbnail((4800, 2400), Image.Resampling.LANCZOS)
        board.paste(img_cropped, (300, y_pos + 120))
        draw.text((600, y_pos + 40), lbl, fill="#24282B", font=font_sub)
        plan_h = 2400

    elif num_plans == 2:
        # Dual Plan Layout: Two large columns
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
        # 3-Floor Layout: Exact Director Sheet 1 Tri-Column Register
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
        # 4+ Plans: Adaptive Multi-Column Register
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

    # 3. Section AA' in lower left
    draw.text((400, y_pos + plan_h + 100), "SECTION AA'", fill="#24282B", font=font_sub)
    section_box = [200, y_pos + plan_h + 200, 5300, sheet_size[1] - 800]
    section_img_path = r"c:\Users\akash\renderize\samples\output_images\output_section.png"
    if os.path.exists(section_img_path):
        sec_img = Image.open(section_img_path).convert("RGB")
        target_w = section_box[2] - section_box[0]
        target_h = section_box[3] - section_box[1]
        sec_img.thumbnail((target_w, target_h), Image.Resampling.LANCZOS)
        board.paste(sec_img, (section_box[0], section_box[1]))
        draw.rectangle(section_box, outline="#24282B", width=3)
    else:
        draw.rectangle(section_box, outline="#A0A5A8", width=3, fill="#FFFFFF")
        draw.text((2200, y_pos + plan_h + 800), "[ SECTION AA' - ELEVATIONAL VIEW ]", fill="#70757A", font=font_sub)

    # 4. Front Elevation Drawing in middle lower right
    draw.text((5600, y_pos + plan_h + 100), "FRONT ELEVATION & CLUSTER PROFILE", fill="#24282B", font=font_sub)
    elev_box = [5500, y_pos + plan_h + 200, 8300, y_pos + plan_h + 1900]
    elev_img_path = r"c:\Users\akash\renderize\samples\output_images\output_elevation.png"
    if os.path.exists(elev_img_path):
        elev_img = Image.open(elev_img_path).convert("RGB")
        target_ew = elev_box[2] - elev_box[0]
        target_eh = elev_box[3] - elev_box[1]
        elev_img.thumbnail((target_ew, target_eh), Image.Resampling.LANCZOS)
        board.paste(elev_img, (elev_box[0], elev_box[1]))
        draw.rectangle(elev_box, outline="#24282B", width=3)

    # 5. Color Palette Swatches (Right side)
    draw.text((8500, y_pos + plan_h + 100), "COLOUR PALETTE", fill="#24282B", font=font_sub)
    swatches = [
        ("#8B5A2B", "Oak Wood"),
        ("#E0E5DF", "Italian Marble"),
        ("#8B9E7A", "Sage Quartzite"),
        ("#363C40", "Charcoal Slate"),
        ("#D0C2B2", "Terrazzo"),
        ("#B8BCB5", "Basalt Paver")
    ]
    sw_y = y_pos + plan_h + 220
    for idx, (color, name) in enumerate(swatches):
        cx = 8550 + (idx % 2) * 550
        cy = sw_y + (idx // 2) * 260
        draw.ellipse([cx, cy, cx + 160, cy + 160], fill=color, outline="#24282B", width=3)
        draw.text((cx - 10, cy + 175), name, fill="#24282B", font=font_info)

    # 6. Project Metadata Title Block (Bottom)
    draw.line([margin, sheet_size[1] - 700, sheet_size[0] - margin, sheet_size[1] - 700], fill="#24282B", width=2)

    total_area_val = 350 * max(1, num_plans)
    info_left = [
        f"TOTAL FLOOR AREA : {total_area_val} SQ.M",
        f"UNIT AREA : 350 SQ.M",
        f"NO. OF BLOCKS : 1",
        f"NO. OF FLOORS : {max(1, num_plans)}",
        f"UNIT TYPOLOGY : 4 BHK + LIBRARY + OFFICE + GUEST"
    ]
    for i, line in enumerate(info_left):
        draw.text((200, sheet_size[1] - 640 + i * 80), line, fill="#24282B", font=font_info)

    draw.text((sheet_size[0] // 2 - 300, sheet_size[1] - 400), "ALL DIMENSIONS ARE IN METRES", fill="#24282B", font=font_info)

    info_right = [
        "SCALE",
        "ROOF PLAN & CLUSTER PLAN :- 1:100",
        "UNIT PLAN :- 1:50",
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

    args = parser.parse_args()
    compose_presentation_sheet(args.plans, output_pdf_path=args.output_pdf, output_png_path=args.output_png)


if __name__ == "__main__":
    main()
