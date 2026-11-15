import pytest
import os
from backend.core.orchestrator import store, execute_rendering_pipeline
from backend.config import SAMPLES_DIR, UPLOADS_DIR
from backend.core.models import ProjectMetadata, ProjectStatus
import shutil
import uuid
from datetime import datetime


def test_multifloor_orchestration(tmp_path):
    p1 = str(SAMPLES_DIR / "DIRECTOR PL PLAN 150.pdf")
    p2 = str(SAMPLES_DIR / "DIRECTOR FL PLAN 150.pdf")
    p3 = str(SAMPLES_DIR / "DIRECTOR SL PLAN 150.pdf")

    project_id = str(uuid.uuid4())[:8]
    saved_paths = []
    for src in [p1, p2, p3]:
        dest = UPLOADS_DIR / f"{project_id}_{os.path.basename(src)}"
        shutil.copy(src, dest)
        saved_paths.append(str(dest))

    project = ProjectMetadata(
        project_id=project_id,
        title="DIRECTOR TEST MULTIFLOOR",
        original_filename="PL, FL, SL PLANS",
        uploaded_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        status=ProjectStatus.QUEUED,
        current_stage="Queued",
        progress_pct=0,
        is_multi_floor=True
    )
    store.set(project)

    # Execute orchestrator directly
    execute_rendering_pipeline(project_id, saved_paths)

    updated = store.get(project_id)
    assert updated.status == ProjectStatus.COMPLETED
    assert updated.progress_pct == 100
    assert len(updated.floors) == 3
    assert "Ground Floor" in updated.floors[0].floor_label
    assert "First Floor" in updated.floors[1].floor_label
    assert "Second Floor" in updated.floors[2].floor_label
    assert updated.validation.verdict == "PASSED"
    assert updated.validation.geometric_fidelity_pct >= 95.0
