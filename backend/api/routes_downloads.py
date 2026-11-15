"""
routes_downloads.py - File Download and Image Serving Endpoints
"""

import os
from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from backend.config import RENDERS_DIR, SAMPLES_DIR
from backend.core.orchestrator import store

router = APIRouter(prefix="/api/projects", tags=["downloads"])


@router.get("/{project_id}/download/{format_type}")
async def download_deliverable(project_id: str, format_type: str):
    """
    Serves rendered deliverables and preview assets:
    - original_preview: PNG of the original line drawing
    - rendered_png: Primary rendered floor plan PNG
    - presentation_png: Full A1 presentation sheet PNG matching DIRECTOR SHEET 1
    - presentation_pdf: Full A1 print-ready presentation PDF matching DIRECTOR SHEET 1
    - qa_overlay: Difference overlay verification image
    - section_png: Longitudinal Section AA'
    - elevation_png: Front Elevation & Cluster Profile
    """
    project = store.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Primary single-floor fallback vs multi-floor floor_0
    orig_path = RENDERS_DIR / f"{project_id}_floor_0_preview.png"
    if not orig_path.exists():
        orig_path = RENDERS_DIR / f"{project_id}_original_preview.png"

    rend_path = RENDERS_DIR / f"{project_id}_floor_0_rendered.png"
    if not rend_path.exists():
        rend_path = RENDERS_DIR / f"{project_id}_rendered.png"

    qa_path = RENDERS_DIR / f"{project_id}_floor_0_rendered_QA_OVERLAY.png"
    if not qa_path.exists():
        qa_path = RENDERS_DIR / f"{project_id}_rendered_QA_OVERLAY.png"

    sec_path = SAMPLES_DIR / "output_images" / "output_section.png"
    elev_path = SAMPLES_DIR / "output_images" / "output_elevation.png"

    file_mapping = {
        "original_preview": (orig_path, "image/png"),
        "rendered_png": (rend_path, "image/png"),
        "presentation_png": (RENDERS_DIR / f"{project_id}_presentation.png", "image/png"),
        "presentation_pdf": (RENDERS_DIR / f"{project_id}_presentation.pdf", "application/pdf"),
        "qa_overlay": (qa_path, "image/png"),
        "section_png": (sec_path, "image/png"),
        "elevation_png": (elev_path, "image/png"),
    }

    if format_type not in file_mapping:
        raise HTTPException(status_code=400, detail=f"Invalid format type: {format_type}")

    file_path, media_type = file_mapping[format_type]
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"Deliverable '{format_type}' is not yet ready.")

    download_filename = f"{project.title}_{format_type}.{'pdf' if 'pdf' in format_type else 'png'}"
    return FileResponse(
        path=str(file_path),
        media_type=media_type,
        filename=download_filename
    )


@router.get("/{project_id}/floors/{floor_idx}/download/{format_type}")
async def download_floor_deliverable(project_id: str, floor_idx: int, format_type: str):
    """Serves individual floor deliverables for multi-floor projects."""
    project = store.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    file_mapping = {
        "original_preview": (RENDERS_DIR / f"{project_id}_floor_{floor_idx}_preview.png", "image/png"),
        "rendered_png": (RENDERS_DIR / f"{project_id}_floor_{floor_idx}_rendered.png", "image/png"),
        "qa_overlay": (RENDERS_DIR / f"{project_id}_floor_{floor_idx}_rendered_QA_OVERLAY.png", "image/png"),
    }

    if format_type not in file_mapping:
        raise HTTPException(status_code=400, detail=f"Invalid floor format: {format_type}")

    file_path, media_type = file_mapping[format_type]
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"Floor {floor_idx} deliverable '{format_type}' not found.")

    floor_label = f"floor_{floor_idx}"
    if floor_idx < len(project.floors):
        floor_label = project.floors[floor_idx].floor_label.replace(" ", "_")

    return FileResponse(
        path=str(file_path),
        media_type=media_type,
        filename=f"{project.title}_{floor_label}_{format_type}.png"
    )
