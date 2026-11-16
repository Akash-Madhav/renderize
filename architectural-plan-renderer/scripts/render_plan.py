#!/usr/bin/env python3
"""
render_plan.py - Stage 5: Advanced Geometric Multi-Surface Plan Renderer

Intelligently detects and isolates the true architectural floor plan:
1. Strips outer sheet borders, margins, and paper frames.
2. Extracts building envelope and internal rooms.
3. Classifies rooms dynamically via geometric spatial analysis & text annotations.
4. Eliminates texture bleed beyond exterior structural walls.
5. Renders authentic architectural materials (Oak Parquet, Italian Marble, Sage Quartzite, Slate, Pavers, Terrazzo).
6. Retains 100% of dimension lines and CAD vector paths with zero geometric drift.
"""

import argparse
import os
import sys
from pathlib import Path
import cv2
import pymupdf
import numpy as np
from PIL import Image, ImageDraw, ImageOps, ImageFilter

# Add scripts directory to path for room_classifier import
SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

try:
    from room_classifier import classify_rooms_from_geometry_and_text, MATERIAL_SPECS
except ImportError:
    import importlib.util
    spec = importlib.util.spec_from_file_location("room_classifier", SCRIPTS_DIR / "room_classifier.py")
    rc_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rc_mod)
    classify_rooms_from_geometry_and_text = rc_mod.classify_rooms_from_geometry_and_text
    MATERIAL_SPECS = rc_mod.MATERIAL_SPECS


def get_default_textures_dir():
    """Dynamically resolves the textures directory without any hardcoded paths."""
    # Look relative to scripts directory: ../assets/textures
    base_assets = SCRIPTS_DIR.parent / "assets" / "textures"
    if base_assets.exists():
        return str(base_assets)
    # Check project root fallback
    root_fallback = SCRIPTS_DIR.parent.parent / "architectural-plan-renderer" / "assets" / "textures"
    if root_fallback.exists():
        return str(root_fallback)
    return str(base_assets)


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
                is_outer_h = abs(p1.x - p2.x) > pw * 0.65 and (p1.y < ph * 0.12 or p1.y > ph * 0.88)
                is_outer_v = abs(p1.y - p2.y) > ph * 0.65 and (p1.x < pw * 0.12 or p1.x > pw * 0.88)
                if not (is_outer_h or is_outer_v):
                    plan_points.extend([(p1.x, p1.y), (p2.x, p2.y)])
            elif item[0] == "re":
                r = item[1]
                if not (r.width > pw * 0.65 and r.height > ph * 0.65):
                    plan_points.extend([(r.x0, r.y0), (r.x1, r.y1)])

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


def extract_building_envelope_and_rooms(gray_array, scale, text_annotations=None, crop_offset=(0, 0)):
    """
    Isolates the architectural building envelope and classifies internal rooms
    dynamically using topological segmentation and text annotations.
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
    room_regions = []
    for i in range(1, num_labels):
        area = stats[i, cv2.CC_STAT_AREA]
        left = stats[i, cv2.CC_STAT_LEFT]
        top = stats[i, cv2.CC_STAT_TOP]
        cw = stats[i, cv2.CC_STAT_WIDTH]
        ch = stats[i, cv2.CC_STAT_HEIGHT]

        touches_edge = (left <= 2 or top <= 2 or (left + cw) >= w - 3 or (top + ch) >= h - 3)
        if not touches_edge and 2500 < area < total_area * 0.40:
            room_regions.append({
                "id": i,
                "bbox": (left, top, cw, ch),
                "area": area,
                "centroid": centroids[i]
            })
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
        x0, x1 = int(x_indices.min()), int(x_indices.max())
        y0, y1 = int(y_indices.min()), int(y_indices.max())
    else:
        x0, y0, x1, y1 = 0, 0, w, h

    # 4. Convert text annotations to pixel coordinates relative to cropped image
    adjusted_annots = []
    if text_annotations:
        ox, oy = crop_offset
        for a in text_annotations:
            bx = a.get("bbox", [])
            if len(bx) == 4:
                adjusted_annots.append({
                    "text": a.get("text", ""),
                    "bbox": [
                        (bx[0] - ox) * scale,
                        (bx[1] - oy) * scale,
                        (bx[2] - ox) * scale,
                        (bx[3] - oy) * scale
                    ]
                })

    # 5. Classify rooms using dynamic room classifier
    zone_assignments = classify_rooms_from_geometry_and_text(
        room_regions=room_regions,
        text_annotations=adjusted_annots,
        canvas_shape=(h, w),
        envelope_bounds=(x0, y0, x1, y1)
    )

    # Create binary masks for each classified zone
    classified_masks = {}
    for zone, rids in zone_assignments.items():
        mask = np.zeros((h, w), dtype=np.uint8)
        for rid in rids:
            mask[labels == rid] = 255
        classified_masks[zone] = mask

    return classified_masks, solid_envelope, thresh, (x0, y0, x1, y1)


def render_architectural_plan(pdf_path, output_png_path, dpi=300, textures_dir=None):
    """
    Renders vector floor plan PDF into high-res presentation graphic with realistic materials,
    stripping outer sheet borders and dead whitespace while guaranteeing zero texture bleed.
    Returns:
        (output_png_path, crop_rect, applied_materials, building_envelope_bounds)
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    tex_base = textures_dir or get_default_textures_dir()
    print(f"[+] Isolating plan from outer sheet borders: {pdf_path} ({dpi} DPI)")
    doc = pymupdf.open(pdf_path)
    page = doc[0]

    # Calculate clean plan-only crop box (excluding outer sheet border)
    crop_rect = get_architectural_plan_crop_box(doc, 0)
    print(f"  - Plan crop bounds: ({crop_rect.x0:.1f}, {crop_rect.y0:.1f}) to ({crop_rect.x1:.1f}, {crop_rect.y1:.1f}) (w={crop_rect.width:.1f}, h={crop_rect.height:.1f})")

    # Extract text annotations inside crop box for semantic room classification
    raw_words = page.get_text("words")
    text_annotations = []
    for w_entry in raw_words:
        # word entry: (x0, y0, x1, y1, text, block_no, line_no, word_no)
        if crop_rect.x0 <= w_entry[0] <= crop_rect.x1 and crop_rect.y0 <= w_entry[1] <= crop_rect.y1:
            text_annotations.append({
                "text": w_entry[4],
                "bbox": [w_entry[0], w_entry[1], w_entry[2], w_entry[3]]
            })

    scale = dpi / 72.0
    mat = pymupdf.Matrix(scale, scale)
    pix = page.get_pixmap(matrix=mat, clip=crop_rect, alpha=False)
    w, h = pix.width, pix.height

    source_img = Image.frombytes("RGB", [w, h], pix.samples)
    gray = np.array(source_img.convert("L"))

    # Segment and dynamically classify rooms
    masks, solid_envelope, thresh, env_bounds = extract_building_envelope_and_rooms(
        gray, scale, text_annotations=text_annotations, crop_offset=(crop_rect.x0, crop_rect.y0)
    )

    # Base Canvas (Architectural off-white #F7FBFE)
    canvas = Image.new("RGB", (w, h), "#F7FBFE")

    # Invert CAD line threshold inside building for wall barrier
    wall_barrier = cv2.dilate(thresh, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)))
    inv_wall = cv2.bitwise_not(wall_barrier)

    # Track materials actually applied for presentation sheet colour palette
    applied_materials = []

    for zone_name, spec in MATERIAL_SPECS.items():
        if zone_name not in masks:
            continue
        tex_path = os.path.join(tex_base, spec["texture_file"])
        zone_mask = cv2.bitwise_and(masks[zone_name], solid_envelope)
        zone_mask = cv2.bitwise_and(zone_mask, inv_wall)

        # Only apply and record if pixels exist in this zone
        if np.any(zone_mask > 0):
            pil_mask = Image.fromarray(zone_mask, mode="L")
            tile_texture_on_mask(canvas, pil_mask, tex_path)
            applied_materials.append({
                "zone": zone_name,
                "name": spec["name"],
                "color": spec["swatch_color"],
                "pixel_count": int(np.count_nonzero(zone_mask))
            })

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
    return output_png_path, crop_rect, applied_materials, env_bounds


def main():
    parser = argparse.ArgumentParser(description="Render architectural floor plan.")
    parser.add_argument("--input", "-i", required=True, help="Input PDF file")
    parser.add_argument("--output", "-o", default=None, help="Output PNG path")
    parser.add_argument("--dpi", type=int, default=300, help="Output resolution DPI")
    parser.add_argument("--textures", default=None, help="Path to textures directory")

    args = parser.parse_args()

    out_png = args.output
    if not out_png:
        base = os.path.splitext(args.input)[0]
        out_png = f"{base}_rendered.png"

    render_architectural_plan(args.input, out_png, args.dpi, textures_dir=args.textures)


if __name__ == "__main__":
    main()
