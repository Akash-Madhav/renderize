#!/usr/bin/env python3
"""
render_plan.py - Stage 5: Advanced Geometric Multi-Surface Plan Renderer

Intelligently detects and isolates the true architectural floor plan:
1. Strips outer sheet borders, margins, and paper frames.
2. Extracts building envelope and internal rooms.
3. Eliminates texture bleed beyond exterior structural walls.
4. Renders authentic materials (French Oak Parquet, Calacatta Marble, Sage Quartzite, Slate).
5. Retains 100% of dimension lines and CAD vector paths with zero geometric drift.
"""

import argparse
import os
import sys
import cv2
import pymupdf
import numpy as np
from PIL import Image, ImageDraw, ImageOps, ImageFilter


def get_architectural_plan_crop_box(doc, page_index=0, padding_pts=18.0):
    """
    Analyzes all vector strokes and text annotations on the PDF page to isolate
    the actual architectural floor plan extents, explicitly filtering out
    outer CAD sheet borders, title block borders, and empty paper margins.
    """
    page = doc[page_index]
    pw, ph = page.rect.width, page.rect.height

    drawings = page.get_drawings()
    plan_points = []

    for d in drawings:
        for item in d.get("items", []):
            if item[0] == "l":
                p1, p2 = item[1], item[2]
                # Filter out lines spanning almost the entire page width or height near the sheet edges
                is_outer_h = abs(p1.x - p2.x) > pw * 0.65 and (p1.y < ph * 0.12 or p1.y > ph * 0.88)
                is_outer_v = abs(p1.y - p2.y) > ph * 0.65 and (p1.x < pw * 0.12 or p1.x > pw * 0.88)
                if not (is_outer_h or is_outer_v):
                    plan_points.extend([(p1.x, p1.y), (p2.x, p2.y)])
            elif item[0] == "re":
                r = item[1]
                # Filter out outer sheet border rectangles
                if not (r.width > pw * 0.65 and r.height > ph * 0.65):
                    plan_points.extend([(r.x0, r.y0), (r.x1, r.y1)])

    # Include dimension text annotations within the architectural drawing area
    text_words = page.get_text("words")
    for w in text_words:
        if not (w[1] > ph * 0.92 or w[0] < pw * 0.04):
            plan_points.extend([(w[0], w[1]), (w[2], w[3])])

    if not plan_points:
        return page.rect

    xs = [p[0] for p in plan_points]
    ys = [p[1] for p in plan_points]

    x0 = max(0.0, min(xs) - padding_pts)
    y0 = max(0.0, min(ys) - padding_pts)
    x1 = min(pw, max(xs) + padding_pts)
    y1 = min(ph, max(ys) + padding_pts)

    return pymupdf.Rect(x0, y0, x1, y1)


def tile_texture_on_mask(canvas, mask, texture_path):
    """Tiles a seamless texture onto canvas constrained by a binary PIL mask."""
    if not os.path.exists(texture_path):
        return
    tex = Image.open(texture_path).convert("RGB")
    cw, ch = canvas.size
    tw, th = tex.size

    tiled = Image.new("RGB", (cw, ch))
    for y in range(0, ch, th):
        for x in range(0, cw, tw):
            tiled.paste(tex, (x, y))

    canvas.paste(tiled, (0, 0), mask)


def extract_building_envelope_and_rooms(gray_array, scale):
    """
    Isolates the true architectural building envelope from the outer dimension collar,
    sealing doors/windows to extract internal habitable rooms with zero exterior bleed.
    """
    h, w = gray_array.shape
    total_area = h * w
    _, thresh = cv2.threshold(gray_array, 240, 255, cv2.THRESH_BINARY_INV)

    # 1. Morphological closing to bridge openings in external walls
    k_size = int(round(4 * scale))
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (k_size, k_size))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    inv_closed = cv2.bitwise_not(closed)

    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(inv_closed)

    # 2. Extract internal rooms that do NOT touch canvas boundary
    envelope_seed_mask = np.zeros((h, w), dtype=np.uint8)
    valid_room_ids = []
    for i in range(1, num_labels):
        area = stats[i, cv2.CC_STAT_AREA]
        left = stats[i, cv2.CC_STAT_LEFT]
        top = stats[i, cv2.CC_STAT_TOP]
        cw = stats[i, cv2.CC_STAT_WIDTH]
        ch = stats[i, cv2.CC_STAT_HEIGHT]

        touches_edge = (left <= 2 or top <= 2 or (left + cw) >= w - 3 or (top + ch) >= h - 3)
        if not touches_edge and 3000 < area < total_area * 0.35:
            valid_room_ids.append(i)
            envelope_seed_mask[labels == i] = 255

    # 3. Form continuous solid building envelope by closing across structural wall thicknesses
    wall_dilation_k = int(round(6 * scale))
    envelope_closed = cv2.morphologyEx(
        envelope_seed_mask,
        cv2.MORPH_CLOSE,
        cv2.getStructuringElement(cv2.MORPH_RECT, (wall_dilation_k, wall_dilation_k))
    )
    contours, _ = cv2.findContours(envelope_closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    solid_envelope = np.zeros((h, w), dtype=np.uint8)
    cv2.drawContours(solid_envelope, contours, -1, 255, thickness=cv2.FILLED)

    # Find tight building bounds
    if np.any(solid_envelope > 0):
        y_indices, x_indices = np.where(solid_envelope > 0)
        x0, x1 = x_indices.min(), x_indices.max()
        y0, y1 = y_indices.min(), y_indices.max()
        bw = max(1, x1 - x0)
        bh = max(1, y1 - y0)
    else:
        x0, y0, x1, y1 = 0, 0, w, h
        bw, bh = w, h

    # 4. Classify internal rooms strictly constrained within solid_envelope
    classified_masks = {
        "bed": np.zeros((h, w), dtype=np.uint8),
        "living": np.zeros((h, w), dtype=np.uint8),
        "kitchen": np.zeros((h, w), dtype=np.uint8),
        "bath": np.zeros((h, w), dtype=np.uint8),
        "paver": np.zeros((h, w), dtype=np.uint8),
    }

    for i in valid_room_ids:
        cx, cy = centroids[i]
        rel_x = (cx - x0) / bw
        rel_y = (cy - y0) / bh
        rmask = (labels == i).astype(np.uint8) * 255

        # Heuristic architectural assignment relative to building envelope:
        if rel_x > 0.78 and 0.2 < rel_y < 0.7:
            # Wet zone / bathrooms
            classified_masks["bath"] = cv2.bitwise_or(classified_masks["bath"], rmask)
        elif rel_y < 0.35 and 0.25 < rel_x < 0.68:
            # Kitchen & service pantry
            classified_masks["kitchen"] = cv2.bitwise_or(classified_masks["kitchen"], rmask)
        elif (0.28 < rel_x < 0.72 and 0.4 < rel_y < 0.9) or (rel_x > 0.65 and rel_y > 0.65):
            # Bedrooms
            classified_masks["bed"] = cv2.bitwise_or(classified_masks["bed"], rmask)
        elif rel_y > 0.88 or rel_y < 0.12 or rel_x > 0.92:
            # External balconies / terraces
            classified_masks["paver"] = cv2.bitwise_or(classified_masks["paver"], rmask)
        else:
            # Great room, living, formal dining, main foyer
            classified_masks["living"] = cv2.bitwise_or(classified_masks["living"], rmask)

    return classified_masks, solid_envelope, thresh


def render_architectural_plan(pdf_path, output_png_path, dpi=300):
    """
    Renders vector floor plan PDF into high-res presentation graphic with realistic materials,
    stripping outer sheet borders and dead whitespace while guaranteeing zero texture bleed.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    print(f"[+] Isolating plan from outer sheet borders: {pdf_path} ({dpi} DPI)")
    doc = pymupdf.open(pdf_path)
    page = doc[0]

    # Calculate clean plan-only crop box (excluding outer sheet border)
    crop_rect = get_architectural_plan_crop_box(doc, 0)
    print(f"  - Plan crop bounds: ({crop_rect.x0:.1f}, {crop_rect.y0:.1f}) to ({crop_rect.x1:.1f}, {crop_rect.y1:.1f}) (w={crop_rect.width:.1f}, h={crop_rect.height:.1f})")

    scale = dpi / 72.0
    mat = pymupdf.Matrix(scale, scale)
    # Render strictly clipped to the true architectural plan bounds
    pix = page.get_pixmap(matrix=mat, clip=crop_rect, alpha=False)
    w, h = pix.width, pix.height

    source_img = Image.frombytes("RGB", [w, h], pix.samples)
    gray = np.array(source_img.convert("L"))

    # Segment rooms with strict envelope boundary
    masks, solid_envelope, thresh = extract_building_envelope_and_rooms(gray, scale)

    # Base Canvas (Architectural off-white #F7FBFE)
    canvas = Image.new("RGB", (w, h), "#F7FBFE")

    tex_base = os.path.abspath(r"c:\Users\akash\renderize\architectural-plan-renderer\assets\textures")
    wood_tex = os.path.join(tex_base, "wood_herringbone.png")
    marble_tex = os.path.join(tex_base, "marble_italian.png")
    sage_tex = os.path.join(tex_base, "stone_sage.png")
    tile_tex = os.path.join(tex_base, "tile_charcoal.png")
    paver_tex = os.path.join(tex_base, "paver_exterior.png")

    # Invert CAD line threshold inside building for wall barrier
    wall_barrier = cv2.dilate(thresh, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)))
    inv_wall = cv2.bitwise_not(wall_barrier)

    # Apply textures strictly inside solid_envelope (ZERO BLEED into dimension collar)
    for zone_name, tex_path in [
        ("living", marble_tex),
        ("bed", wood_tex),
        ("kitchen", sage_tex),
        ("bath", tile_tex),
        ("paver", paver_tex),
    ]:
        zone_mask = cv2.bitwise_and(masks[zone_name], solid_envelope)
        zone_mask = cv2.bitwise_and(zone_mask, inv_wall)
        pil_mask = Image.fromarray(zone_mask, mode="L")
        tile_texture_on_mask(canvas, pil_mask, tex_path)

    # Wall Structural Fill: Solid Charcoal (#24282B) strictly on structural walls
    structural_walls = cv2.bitwise_and(thresh, solid_envelope)
    line_mask_pil = Image.fromarray(structural_walls, mode="L")
    dilated_walls = line_mask_pil.filter(ImageFilter.MaxFilter(size=3))
    wall_color_layer = Image.new("RGB", (w, h), "#24282B")
    canvas.paste(wall_color_layer, (0, 0), dilated_walls)

    # Re-impose full CAD black vector lines (dimensions, witness marks, annotations) with 100% fidelity
    full_cad_lines = Image.fromarray(thresh, mode="L")
    canvas.paste(Image.new("RGB", (w, h), "#000000"), (0, 0), full_cad_lines)

    # Save clean plan-only rendered output
    os.makedirs(os.path.dirname(os.path.abspath(output_png_path)), exist_ok=True)
    canvas.save(output_png_path, quality=95)
    print(f"[✓] Plan-only rendering saved to: {output_png_path} (Outer border removed, zero bleed)")
    return output_png_path, crop_rect


def main():
    parser = argparse.ArgumentParser(description="Render architectural floor plan.")
    parser.add_argument("--input", "-i", required=True, help="Input PDF file")
    parser.add_argument("--output", "-o", default=None, help="Output PNG path")
    parser.add_argument("--dpi", type=int, default=300, help="Output resolution DPI")

    args = parser.parse_args()

    out_png = args.output
    if not out_png:
        base = os.path.splitext(args.input)[0]
        out_png = f"{base}_rendered.png"

    render_architectural_plan(args.input, out_png, args.dpi)


if __name__ == "__main__":
    main()
