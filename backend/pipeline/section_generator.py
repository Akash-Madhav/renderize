"""
section_generator.py - Wrapper for Stage 5B: Dynamic Section AA' Generation
"""

import sys
import os
from pathlib import Path
from typing import List, Dict, Any
from backend.config import SKILL_SCRIPTS_DIR

sys.path.insert(0, str(SKILL_SCRIPTS_DIR))

try:
    from generate_section import generate_dynamic_section
except ImportError:
    import importlib.util
    spec = importlib.util.spec_from_file_location("generate_section", SKILL_SCRIPTS_DIR / "generate_section.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    generate_dynamic_section = mod.generate_dynamic_section


def run_section_generation(floor_data: List[Dict[str, Any]], output_path: str, project_title: str = "RESIDENCE") -> str:
    """Generates an authentic longitudinal Section AA' graphic dynamically."""
    return generate_dynamic_section(floor_data, output_path, project_title=project_title)
