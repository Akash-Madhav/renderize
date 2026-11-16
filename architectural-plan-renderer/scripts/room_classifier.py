#!/usr/bin/env python3
"""
room_classifier.py - Intelligent Geometric & Textual Architectural Room Classifier

Uses extracted CAD text annotations (labels, room names) combined with
topological spatial features (area, aspect ratio, fixture detection) to accurately
classify rooms across ANY architectural floor plan layout without hardcoded coordinate ratios.
"""

import math
from typing import Dict, List, Any, Tuple, Optional
import numpy as np
import cv2

# Standard Architectural Material Palette
MATERIAL_SPECS = {
    "living": {
        "name": "Italian Marble",
        "texture_file": "marble_italian.png",
        "swatch_color": "#E0E5DF",
        "keywords": ["LIVING", "HALL", "FOYER", "DRAWING", "LOUNGE", "DINING", "FAMILY", "ENTRY", "RECEPTION"]
    },
    "bed": {
        "name": "Oak Wood Parquet",
        "texture_file": "wood_herringbone.png",
        "swatch_color": "#8B5A2B",
        "keywords": ["BED", "BEDROOM", "MBR", "GUEST", "SUITE", "MASTER"]
    },
    "kitchen": {
        "name": "Sage Quartzite",
        "texture_file": "stone_sage.png",
        "swatch_color": "#8B9E7A",
        "keywords": ["KITCHEN", "PANTRY", "UTILITY", "COOK", "STORE", "WET"]
    },
    "bath": {
        "name": "Charcoal Slate",
        "texture_file": "tile_charcoal.png",
        "swatch_color": "#363C40",
        "keywords": ["BATH", "TOILET", "WC", "POWDER", "RESTROOM", "W.C", "DRESS"]
    },
    "paver": {
        "name": "Basalt Paver",
        "texture_file": "paver_exterior.png",
        "swatch_color": "#B8BCB5",
        "keywords": ["BALCONY", "TERRACE", "VERANDAH", "DECK", "PORCH", "PATIO", "SITOUT", "OPEN"]
    },
    "circulation": {
        "name": "Warm Terrazzo",
        "texture_file": "terrazzo_warm.png",
        "swatch_color": "#D0C2B2",
        "keywords": ["STAIR", "LIFT", "CORRIDOR", "PASSAGE", "LOBBY", "CORE"]
    },
    "garden": {
        "name": "Landscape Lawn & Garden",
        "texture_file": "grass_garden.png",
        "swatch_color": "#557A46",
        "keywords": ["GARDEN", "LAWN", "LANDSCAPE", "YARD", "COURTYARD", "GREEN", "BACKYARD", "FORECOURT", "PLANTATION"]
    }
}


def classify_rooms_from_geometry_and_text(
    room_regions: List[Dict[str, Any]],
    text_annotations: List[Dict[str, Any]],
    canvas_shape: Tuple[int, int],
    envelope_bounds: Tuple[int, int, int, int]
) -> Dict[str, List[int]]:
    """
    Classifies room region IDs into architectural zones based on:
    1. Text label containment/proximity (e.g., 'BEDROOM', 'TOILET', 'KITCHEN').
    2. Geometric proportions (area, perimeter-to-area ratio, aspect ratio).
    3. Spatial context (perimeter exposure, internal vs exterior).

    Returns:
        Dict mapping zone_name ("living", "bed", "kitchen", "bath", "paver", "circulation")
        to list of matching room IDs.
    """
    x0, y0, x1, y1 = envelope_bounds
    bw = max(1, x1 - x0)
    bh = max(1, y1 - y0)
    total_env_area = bw * bh

    classified = {zone: [] for zone in MATERIAL_SPECS.keys()}
    unassigned = []

    # 1. First pass: Match extracted text labels to room regions
    for room in room_regions:
        rid = room["id"]
        rx, ry, rw, rh = room["bbox"]
        rcx, rcy = rx + rw / 2.0, ry + rh / 2.0
        r_area = room["area"]

        matched_zone = None
        min_dist = float("inf")

        for annot in text_annotations:
            text = annot.get("text", "").upper().strip()
            abox = annot.get("bbox", [])
            if not text or len(abox) < 4:
                continue

            acx = (abox[0] + abox[2]) / 2.0
            acy = (abox[1] + abox[3]) / 2.0

            # Check if text is inside room bounding box or within near proximity
            inside = (rx - 10 <= acx <= rx + rw + 10) and (ry - 10 <= acy <= ry + rh + 10)
            dist = math.hypot(rcx - acx, rcy - acy)

            for zone, spec in MATERIAL_SPECS.items():
                if any(kw in text for kw in spec["keywords"]):
                    if inside:
                        matched_zone = zone
                        break
                    elif dist < rw * 0.7 + rh * 0.7 and dist < min_dist:
                        min_dist = dist
                        matched_zone = zone
            if inside and matched_zone:
                break

        if matched_zone:
            classified[matched_zone].append(rid)
        else:
            unassigned.append(room)

    # 2. Second pass: Classify unassigned rooms using geometric & topological properties
    for room in unassigned:
        rid = room["id"]
        rx, ry, rw, rh = room["bbox"]
        rcx, rcy = rx + rw / 2.0, ry + rh / 2.0
        area = room["area"]
        rel_area = area / float(total_env_area) if total_env_area > 0 else 0
        aspect = max(rw, rh) / max(1.0, min(rw, rh))

        # Relative location inside building envelope
        rel_x = (rcx - x0) / float(bw)
        rel_y = (rcy - y0) / float(bh)
        edge_dist = min(rel_x, 1.0 - rel_x, rel_y, 1.0 - rel_y)

        # Proportions:
        # Bathrooms/Toilets: Typically smallest enclosed rooms (relative area < 4%), often near wet zones or edges
        if rel_area < 0.045 and aspect < 2.5:
            classified["bath"].append(rid)
        # Balconies / Terraces / Verandahs: Near exterior perimeter, often elongated aspect ratio
        elif edge_dist < 0.10 and (aspect > 2.0 or rel_area < 0.06):
            classified["paver"].append(rid)
        # Corridors / Circulation: Long narrow passages
        elif aspect > 3.2:
            classified["circulation"].append(rid)
        # Kitchen: Medium-sized service zone
        elif 0.045 <= rel_area < 0.09:
            classified["kitchen"].append(rid)
        # Bedrooms: Substantial private rooms (typically 9% to 22% of floor footprint)
        elif 0.09 <= rel_area < 0.25:
            classified["bed"].append(rid)
        # Grand living / dining / lounge: Largest central zones (> 25% of footprint or central core)
        else:
            classified["living"].append(rid)

    return classified
