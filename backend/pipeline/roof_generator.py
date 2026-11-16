"""
roof_generator.py - Wrapper for Stage 5D: Dynamic Roof Plan Generation
"""

import sys
import os
from pathlib import Path
from backend.config import SKILL_SCRIPTS_DIR

sys.path.insert(0, str(SKILL_SCRIPTS_DIR))

try:
    from generate_roof import generate_dynamic_roof_plan
except ImportError:
    import importlib.util
    spec = importlib.util.spec_from_file_location("generate_roof", SKILL_SCRIPTS_DIR / "generate_roof.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    generate_dynamic_roof_plan = mod.generate_dynamic_roof_plan


def run_roof_generation(output_path: str, project_title: str = "RESIDENCE") -> str:
    """Generates an authentic Roof & Cluster Plan graphic dynamically."""
    return generate_dynamic_roof_plan(output_path, project_title=project_title)
