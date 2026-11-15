"""
config.py - Renderize Global Backend Configuration
"""

import os
from pathlib import Path

# Base Paths
BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BACKEND_DIR.parent
SKILL_DIR = PROJECT_ROOT / "architectural-plan-renderer"
SAMPLES_DIR = PROJECT_ROOT / "samples"

# Skill Subdirectories
SKILL_SCRIPTS_DIR = SKILL_DIR / "scripts"
SKILL_ASSETS_DIR = SKILL_DIR / "assets"
SKILL_TEXTURES_DIR = SKILL_ASSETS_DIR / "textures"
SKILL_FURNITURE_DIR = SKILL_ASSETS_DIR / "furniture"
SKILL_TEMPLATES_DIR = SKILL_ASSETS_DIR / "templates"
SKILL_REFERENCES_DIR = SKILL_DIR / "references"

# Persistent Storage Directories
STORAGE_DIR = BACKEND_DIR / "storage"
UPLOADS_DIR = STORAGE_DIR / "uploads"
RENDERS_DIR = STORAGE_DIR / "renders"
MODELS_DIR = STORAGE_DIR / "models"
REPORTS_DIR = STORAGE_DIR / "reports"

# Ensure all storage directories exist
for d in [UPLOADS_DIR, RENDERS_DIR, MODELS_DIR, REPORTS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Processing Parameters
DEFAULT_DPI = 300
GEOMETRIC_TOLERANCE_PX = 2
FIDELITY_PASS_THRESHOLD_PCT = 95.0
MAX_CORRECTION_ITERATIONS = 3

# Server Settings
HOST = "127.0.0.1"
PORT = 8000
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000"
]
