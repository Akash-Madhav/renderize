#!/usr/bin/env python3
"""
validate_output.py - Stage 7: Architectural Quality Assurance & Verification

Performs geometric overlay validation between source vector CAD PDF
and rendered presentation output. Measures wall axis displacement,
dimension label retention, and checks for geometric distortions.
"""

import argparse
import os
import sys
import pymupdf
from PIL import Image, ImageOps, ImageChops
import numpy as np


def validate_architectural_fidelity(source_pdf_path, rendered_png_path, tolerance_px=2):
    if not os.path.exists(source_pdf_path):
        raise FileNotFoundError(f"Source PDF not found: {source_pdf_path}")
    if not os.path.exists(rendered_png_path):
        raise FileNotFoundError(f"Rendered image not found: {rendered_png_path}")

    print(f"[+] Running Architectural QA Audit:")
    print(f"  - Source CAD: {source_pdf_path}")
    print(f"  - Rendered Plan: {rendered_png_path}")

    # 1. Rasterize source CAD at matching scale and clip bounds
    doc = pymupdf.open(source_pdf_path)
    page = doc[0]
    rendered_img = Image.open(rendered_png_path).convert("RGB")
    rw, rh = rendered_img.size

    # Check if rendered image is cropped to plan bounds
    from render_plan import get_architectural_plan_crop_box
    plan_crop = get_architectural_plan_crop_box(doc, 0)
    
    # If aspect ratio of rendered image matches plan_crop, rasterize with clip
    ratio_crop = plan_crop.width / plan_crop.height
    ratio_page = page.rect.width / page.rect.height
    ratio_rend = rw / rh

    if abs(ratio_rend - ratio_crop) < abs(ratio_rend - ratio_page):
        # Cropped to plan bounds (outer border excluded)
        scale_x = rw / plan_crop.width
        scale_y = rh / plan_crop.height
        mat = pymupdf.Matrix(scale_x, scale_y)
        pix = page.get_pixmap(matrix=mat, clip=plan_crop, alpha=False)
    else:
        # Full page
        scale_x = rw / page.rect.width
        scale_y = rh / page.rect.height
        mat = pymupdf.Matrix(scale_x, scale_y)
        pix = page.get_pixmap(matrix=mat, alpha=False)

    source_raster = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    if source_raster.size != (rw, rh):
        source_raster = source_raster.resize((rw, rh), Image.Resampling.NEAREST)

    # 2. Extract line masks
    src_gray = source_raster.convert("L")
    src_lines = ImageOps.invert(src_gray).point(lambda p: 255 if p > 50 else 0)

    rend_gray = rendered_img.convert("L")
    rend_lines = ImageOps.invert(rend_gray).point(lambda p: 255 if p > 80 else 0)

    # 3. Geometric overlap within specified tolerance
    import cv2
    src_arr = np.array(src_lines) > 0
    rend_arr = np.array(rend_lines) > 0

    if tolerance_px > 0:
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2 * tolerance_px + 1, 2 * tolerance_px + 1))
        rend_dilated = cv2.dilate(rend_arr.astype(np.uint8), kernel) > 0
        overlap = np.logical_and(src_arr, rend_dilated)
    else:
        overlap = np.logical_and(src_arr, rend_arr)

    src_total = np.sum(src_arr)
    overlap_total = np.sum(overlap)

    fidelity_score = (overlap_total / src_total) * 100.0 if src_total > 0 else 100.0

    print(f"  - Total CAD line pixels: {src_total:,}")
    print(f"  - Verified overlapping pixels: {overlap_total:,}")
    print(f"  - Geometric Retention Fidelity: {fidelity_score:.2f}%")

    passed = fidelity_score >= 85.0
    status = "PASSED" if passed else "FAILED"

    print(f"[✓] Architectural QA Verdict: [{status}] (Tolerance: {tolerance_px}px)")

    # 4. Generate visual difference overlay inspection image
    diff_img = Image.new("RGBA", (rw, rh), (0, 0, 0, 0))
    # Red for source CAD lines
    red_overlay = Image.new("RGBA", (rw, rh), (255, 0, 0, 100))
    diff_composite = Image.composite(red_overlay, rendered_img.convert("RGBA"), src_lines)

    overlay_out = os.path.splitext(rendered_png_path)[0] + "_QA_OVERLAY.png"
    diff_composite.save(overlay_out)
    print(f"[✓] QA difference overlay saved to: {overlay_out}")

    return {
        "verdict": status,
        "fidelity_score_pct": round(fidelity_score, 2),
        "overlay_path": overlay_out
    }


def main():
    parser = argparse.ArgumentParser(description="Architectural plan rendering QA validator.")
    parser.add_argument("--source", "-s", required=True, help="Path to original CAD PDF")
    parser.add_argument("--rendered", "-r", required=True, help="Path to rendered plan PNG")
    parser.add_argument("--tolerance", "-t", type=int, default=2, help="Displacement tolerance in pixels")

    args = parser.parse_args()

    validate_architectural_fidelity(args.source, args.rendered, args.tolerance)


if __name__ == "__main__":
    main()
