"""
routes_projects.py - FastAPI Routes for Project Management & Multi-Floor Pipeline Triggers
"""

import os
import uuid
import shutil
from datetime import datetime
from typing import List, Optional
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException

from backend.config import UPLOADS_DIR, SAMPLES_DIR
from backend.core.models import ProjectMetadata, ProjectStatus
from backend.core.orchestrator import store, execute_rendering_pipeline

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.post("", response_model=ProjectMetadata, status_code=201)
async def create_project(background_tasks: BackgroundTasks, files: List[UploadFile] = File(...)):
    """
    Upload one or multiple architectural floor plan PDFs and initiate the rendering pipeline.
    """
    if not files:
        raise HTTPException(status_code=400, detail="At least one PDF file must be provided.")

    for f in files:
        if not f.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail=f"File '{f.filename}' is not an architectural PDF.")

    project_id = str(uuid.uuid4())[:8]
    saved_paths = []

    for f in files:
        saved_filename = f"{project_id}_{f.filename}"
        saved_pdf_path = UPLOADS_DIR / saved_filename
        with open(saved_pdf_path, "wb") as buffer:
            shutil.copyfileobj(f.file, buffer)
        saved_paths.append(str(saved_pdf_path))

    title = os.path.splitext(files[0].filename)[0] if len(files) == 1 else f"Multi-Floor Project ({len(files)} Levels)"

    # Initialize project state
    project = ProjectMetadata(
        project_id=project_id,
        title=title,
        original_filename=", ".join(f.filename for f in files),
        uploaded_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        status=ProjectStatus.QUEUED,
        current_stage=f"Stage 0/10: Initializing Ingestion for {len(files)} file{'s' if len(files) > 1 else ''}",
        progress_pct=5,
        is_multi_floor=(len(files) > 1),
        logs=[f"Project created with ID {project_id} containing {len(files)} architectural floor(s)"]
    )
    store.set(project)

    # Dispatch asynchronous rendering task
    background_tasks.add_task(execute_rendering_pipeline, project_id, saved_paths)

    return project


@router.post("/demo-multi-floor", response_model=ProjectMetadata, status_code=201)
async def create_demo_multi_floor_project(background_tasks: BackgroundTasks):
    """
    Instantly spins up the complete 3-floor Director Residence project
    (Ground Floor, First Floor, Second Floor) and composes DIRECTOR SHEET 1.
    """
    sample_files = [
        "DIRECTOR PL PLAN 150.pdf",
        "DIRECTOR FL PLAN 150.pdf",
        "DIRECTOR SL PLAN 150.pdf"
    ]

    project_id = str(uuid.uuid4())[:8]
    saved_paths = []

    for s_name in sample_files:
        src = SAMPLES_DIR / s_name
        if not src.exists():
            raise HTTPException(status_code=500, detail=f"Reference sample '{s_name}' not found on server.")
        dest = UPLOADS_DIR / f"{project_id}_{s_name}"
        shutil.copy(src, dest)
        saved_paths.append(str(dest))

    project = ProjectMetadata(
        project_id=project_id,
        title="DIRECTOR RESIDENCE (Master 3-Floor Sheet)",
        original_filename="DIRECTOR PL, FL, SL PLANS",
        uploaded_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        status=ProjectStatus.QUEUED,
        current_stage="Stage 0/10: Loading 3-Floor Architectural CAD Set",
        progress_pct=5,
        is_multi_floor=True,
        logs=[f"Initialized 3-Floor Director Residence Demonstration Project with ID {project_id}"]
    )
    store.set(project)

    background_tasks.add_task(execute_rendering_pipeline, project_id, saved_paths)
    return project


@router.get("", response_model=List[ProjectMetadata])
async def list_projects():
    """Returns a list of all historical rendering projects."""
    return store.list_all()


@router.get("/{project_id}", response_model=ProjectMetadata)
async def get_project(project_id: str):
    """Retrieve full project state, telemetry, floor renders, and deliverable URLs."""
    project = store.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.get("/{project_id}/status")
async def get_project_status(project_id: str):
    """Lightweight polling endpoint for live UI stepper progress."""
    project = store.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return {
        "project_id": project.project_id,
        "status": project.status,
        "current_stage": project.current_stage,
        "progress_pct": project.progress_pct,
        "is_multi_floor": project.is_multi_floor,
        "floors_count": len(project.floors),
        "logs": project.logs[-8:],
        "error_message": project.error_message
    }


@router.delete("/{project_id}", status_code=200)
async def delete_project(project_id: str):
    """Deletes a specific project and all its generated files on disk."""
    deleted = store.delete(project_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"status": "success", "message": f"Project '{project_id}' deleted successfully."}


@router.delete("", status_code=200)
async def delete_all_projects():
    """Deletes all projects and wipes all cached render artifacts."""
    store.delete_all()
    return {"status": "success", "message": "All projects and render artifacts deleted successfully."}
