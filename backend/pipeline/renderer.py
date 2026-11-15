"""
renderer.py - Wrapper for Stage 5: Multi-Surface Plan Rendering

Directly binds architectural-plan-renderer/scripts/render_plan.py
"""

import sys
import os
from pathlib import Path
from backend.config import SKILL_SCRIPTS_DIR

sys.path.insert(0, str(SKILL_SCRIPTS_DIR))

try:
    from render_plan import render_architectural_plan, get_architectural_plan_crop_box
except ImportError:
    import importlib.util
    spec = importlib.util.spec_from_file_location("render_plan", SKILL_SCRIPTS_DIR / "render_plan.py")
    render_plan_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(render_plan_module)
    render_architectural_plan = render_plan_module.render_architectural_plan
    get_architectural_plan_crop_box = render_plan_module.get_architectural_plan_crop_box


def run_render(pdf_path: str, output_png_path: str, dpi: int = 300):
    """Renders a vector floor plan PDF into high-res presentation graphic with realistic materials."""
    res = render_architectural_plan(pdf_path, output_png_path, dpi=dpi)
    if isinstance(res, tuple):
        return res[0], res[1]
    return res, None
