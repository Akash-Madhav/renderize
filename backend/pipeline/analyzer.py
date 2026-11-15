"""
analyzer.py - Wrapper for Stage 2: Geometric & Spatial Analysis

Directly binds architectural-plan-renderer/scripts/analyze_geometry.py
"""

import sys
import os
from pathlib import Path
from backend.config import SKILL_SCRIPTS_DIR

sys.path.insert(0, str(SKILL_SCRIPTS_DIR))

try:
    from analyze_geometry import analyze_extracted_primitives
except ImportError:
    import importlib.util
    spec = importlib.util.spec_from_file_location("analyze_geometry", SKILL_SCRIPTS_DIR / "analyze_geometry.py")
    analyze_geom_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(analyze_geom_module)
    analyze_extracted_primitives = analyze_geom_module.analyze_extracted_primitives


def run_geometry_analysis(extracted_json_path: str, output_model_path: str) -> dict:
    """Decomposes extracted vector paths into walls, room boundaries, and annotations."""
    return analyze_extracted_primitives(extracted_json_path, output_model_path)
