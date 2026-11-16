"""
elevation_generator.py - Wrapper for Stage 5C: Dynamic Front Elevation Generation
"""

import sys
import os
from pathlib import Path
from typing import List, Dict, Any
from backend.config import SKILL_SCRIPTS_DIR

sys.path.insert(0, str(SKILL_SCRIPTS_DIR))

try:
    from generate_elevation import generate_dynamic_elevation
except ImportError:
    import importlib.util
    spec = importlib.util.spec_from_file_location("generate_elevation", SKILL_SCRIPTS_DIR / "generate_elevation.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    generate_dynamic_elevation = mod.generate_dynamic_elevation


def run_elevation_generation(floor_data: List[Dict[str, Any]], output_path: str, project_title: str = "RESIDENCE") -> str:
    """Generates an authentic Front Elevation & Cluster Profile graphic dynamically."""
    return generate_dynamic_elevation(floor_data, output_path, project_title=project_title)
