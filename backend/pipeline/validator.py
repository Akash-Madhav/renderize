"""
validator.py - Wrapper for Stage 7: Architectural Quality Assurance

Directly binds architectural-plan-renderer/scripts/validate_output.py
"""

import sys
import os
from pathlib import Path
from backend.config import SKILL_SCRIPTS_DIR

sys.path.insert(0, str(SKILL_SCRIPTS_DIR))

try:
    from validate_output import validate_architectural_fidelity
except ImportError:
    import importlib.util
    spec = importlib.util.spec_from_file_location("validate_output", SKILL_SCRIPTS_DIR / "validate_output.py")
    validate_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(validate_module)
    validate_architectural_fidelity = validate_module.validate_architectural_fidelity


def run_validation(source_pdf: str, rendered_png: str, tolerance_px: int = 2) -> dict:
    """Verifies geometric line preservation, wall alignment, and retention fidelity."""
    return validate_architectural_fidelity(source_pdf, rendered_png, tolerance_px)
