"""
extractor.py - Wrapper for Stage 1: Vector Extraction

Directly binds architectural-plan-renderer/scripts/extract_pdf.py
"""

import sys
import os
from pathlib import Path
from backend.config import SKILL_SCRIPTS_DIR

# Add skill scripts directory to sys.path
sys.path.insert(0, str(SKILL_SCRIPTS_DIR))

try:
    from extract_pdf import extract_pdf_data
except ImportError:
    # Direct import fallback
    import importlib.util
    spec = importlib.util.spec_from_file_location("extract_pdf", SKILL_SCRIPTS_DIR / "extract_pdf.py")
    extract_pdf_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(extract_pdf_module)
    extract_pdf_data = extract_pdf_module.extract_pdf_data


def run_extraction(pdf_path: str, output_json_path: str) -> dict:
    """Extracts raw primitives, line segments, and dimensions from an architectural vector PDF."""
    return extract_pdf_data(pdf_path, output_json_path)
