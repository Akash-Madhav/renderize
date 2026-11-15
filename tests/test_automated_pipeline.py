import pytest
import os
import sys

sys.path.insert(0, r"c:\Users\akash\renderize")

from backend.pipeline.extractor import run_extraction
from backend.pipeline.analyzer import run_geometry_analysis
from backend.pipeline.renderer import run_render
from backend.pipeline.validator import run_validation
from backend.pipeline.compositor import run_composition
from backend.ai.gemma_service import gemma_ai

SAMPLE_PL = r"c:\Users\akash\renderize\samples\DIRECTOR PL PLAN 150.pdf"
SAMPLE_FL = r"c:\Users\akash\renderize\samples\DIRECTOR FL PLAN 150.pdf"
SAMPLE_SL = r"c:\Users\akash\renderize\samples\DIRECTOR SL PLAN 150.pdf"


def test_extraction_stage(tmp_path):
    out_json = str(tmp_path / "ext.json")
    data = run_extraction(SAMPLE_PL, out_json)
    assert data["total_pages"] == 1
    p0 = data["pages"][0]
    assert p0["paths_count"] > 8000
    assert p0["annotations_count"] > 20
    assert os.path.exists(out_json)


def test_geometric_analyzer_stage(tmp_path):
    ext_json = str(tmp_path / "ext.json")
    ana_json = str(tmp_path / "ana.json")
    run_extraction(SAMPLE_PL, ext_json)
    model = run_geometry_analysis(ext_json, ana_json)
    assert model["drawing_type"] == "FLOOR_PLAN"
    assert len(model["dimensions"]["annotations"]) > 10
    assert model["spatial_decomposition"]["has_stairs"] is True


def test_gemma_ai_reasoning():
    mock_model = {"source_file": "DIRECTOR PL PLAN 150.pdf"}
    res = gemma_ai.infer_plan_semantics(mock_model)
    assert "RESIDENCE" in res.project_typology
    assert len(res.rooms) >= 5
    assert any(r.semantic_type.value == "KITCHEN" for r in res.rooms)
    assert any(r.semantic_type.value == "BEDROOM" for r in res.rooms)


def test_rendering_and_geometric_fidelity(tmp_path):
    rend_png = str(tmp_path / "rendered.png")
    run_render(SAMPLE_PL, rend_png, dpi=150)
    assert os.path.exists(rend_png)

    val = run_validation(SAMPLE_PL, rend_png)
    assert val["fidelity_score_pct"] >= 95.0
    assert val["verdict"] == "PASSED"
    assert os.path.exists(val["overlay_path"])


def test_multi_floor_composition(tmp_path):
    rend_pl = str(tmp_path / "pl.png")
    rend_fl = str(tmp_path / "fl.png")
    rend_sl = str(tmp_path / "sl.png")
    out_pdf = str(tmp_path / "board.pdf")
    out_png = str(tmp_path / "board.png")

    run_render(SAMPLE_PL, rend_pl, dpi=100)
    run_render(SAMPLE_FL, rend_fl, dpi=100)
    run_render(SAMPLE_SL, rend_sl, dpi=100)

    run_composition(rend_pl, rend_fl, rend_sl, out_pdf, out_png)
    assert os.path.exists(out_pdf)
    assert os.path.exists(out_png)
    assert os.path.getsize(out_pdf) > 50000
