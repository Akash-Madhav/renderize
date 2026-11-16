"""
compositor.py - Wrapper for Stage 6: Presentation Sheet Composition

Directly binds architectural-plan-renderer/scripts/compose_sheet.py
"""

import sys
import os
from typing import List, Union, Optional, Dict, Any
from pathlib import Path
from backend.config import SKILL_SCRIPTS_DIR

sys.path.insert(0, str(SKILL_SCRIPTS_DIR))

try:
    from compose_sheet import compose_presentation_sheet
except ImportError:
    import importlib.util
    spec = importlib.util.spec_from_file_location("compose_sheet", SKILL_SCRIPTS_DIR / "compose_sheet.py")
    compose_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(compose_module)
    compose_presentation_sheet = compose_module.compose_presentation_sheet


def run_composition(
    plans_input: Union[List, str],
    first_png: str = None,
    second_png: str = None,
    output_pdf: str = None,
    output_png: str = None,
    project_title: str = "ARCHITECTURAL RESIDENCE",
    section_image_path: Optional[str] = None,
    elevation_image_path: Optional[str] = None,
    applied_materials: Optional[List[Dict[str, Any]]] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> str:
    """Assembles arbitrary N rendered floor plans into an A1 presentation board PDF & PNG."""
    return compose_presentation_sheet(
        plans_input,
        first_plan_path=first_png,
        second_plan_path=second_png,
        output_pdf_path=output_pdf,
        output_png_path=output_png,
        project_title=project_title,
        section_image_path=section_image_path,
        elevation_image_path=elevation_image_path,
        applied_materials=applied_materials,
        metadata=metadata
    )
