"""
models.py - Pydantic Schemas for Projects, Pipeline States, and Validation Reports
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class ProjectStatus(str, Enum):
    QUEUED = "QUEUED"
    EXTRACTING_PDF = "EXTRACTING_PDF"
    ANALYZING_GEOMETRY = "ANALYZING_GEOMETRY"
    SEMANTIC_REASONING = "SEMANTIC_REASONING"
    RENDERING_MATERIALS = "RENDERING_MATERIALS"
    VALIDATING_OUTPUT = "VALIDATING_OUTPUT"
    APPLYING_CORRECTIONS = "APPLYING_CORRECTIONS"
    COMPOSING_SHEET = "COMPOSING_SHEET"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class SemanticRoomType(str, Enum):
    BEDROOM = "BEDROOM"
    KITCHEN = "KITCHEN"
    BATHROOM = "BATHROOM"
    LIVING_DINING = "LIVING_DINING"
    OFFICE_STUDY = "OFFICE_STUDY"
    CIRCULATION = "CIRCULATION"
    BALCONY_TERRACE = "BALCONY_TERRACE"
    DOUBLE_HEIGHT_VOID = "DOUBLE_HEIGHT_VOID"
    COURTYARD_GARDEN = "COURTYARD_GARDEN"


class RecommendedFlooring(str, Enum):
    WOOD_PARQUET_HERRINGBONE = "WOOD_PARQUET_HERRINGBONE"
    STONE_MARBLE_ITALIAN = "STONE_MARBLE_ITALIAN"
    STONE_VERDE_SAGE = "STONE_VERDE_SAGE"
    TILE_CHARCOAL_SLATE = "TILE_CHARCOAL_SLATE"
    TERRAZZO_WARM = "TERRAZZO_WARM"
    PAVER_EXTERIOR = "PAVER_EXTERIOR"
    OPEN_AIR = "OPEN_AIR"
    LANDSCAPE_GARDEN_LAWN = "LANDSCAPE_GARDEN_LAWN"


class RoomSemanticAnalysis(BaseModel):
    room_id: str
    semantic_type: SemanticRoomType
    subtype: str
    recommended_flooring: RecommendedFlooring
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str


class PlanSemanticInferenceResponse(BaseModel):
    project_typology: str
    rooms: List[RoomSemanticAnalysis]
    unidentified_zones: List[str] = []


class ValidationReport(BaseModel):
    geometric_fidelity_pct: float
    wall_axis_max_displacement_px: float
    elements_detected: Dict[str, int] = {}
    elements_retained_pct: float = 100.0
    correction_iterations_run: int = 0
    unresolved_discrepancies: List[str] = []
    verdict: str  # "PASSED" or "FLAGGED_FOR_REVIEW"
    overlay_image_url: Optional[str] = None


class FloorPlanInfo(BaseModel):
    floor_id: str
    floor_label: str
    original_filename: str
    preview_original_url: str
    rendered_image_url: str
    qa_overlay_url: str
    fidelity_score_pct: float = 100.0
    extracted_paths_count: int = 0
    annotations_count: int = 0
    dimensions_detected: List[str] = []
    rooms: List[RoomSemanticAnalysis] = []


class ProjectMetadata(BaseModel):
    project_id: str
    title: str
    original_filename: str
    uploaded_at: str
    status: ProjectStatus
    current_stage: str
    progress_pct: int
    dimensions_pts: Optional[List[float]] = None
    extracted_paths_count: Optional[int] = None
    annotations_count: Optional[int] = None
    dimensions_detected: List[str] = []
    semantic_typology: Optional[str] = None
    rooms: List[RoomSemanticAnalysis] = []
    validation: Optional[ValidationReport] = None
    preview_original_url: Optional[str] = None
    rendered_image_url: Optional[str] = None
    presentation_pdf_url: Optional[str] = None
    presentation_png_url: Optional[str] = None
    floors: List[FloorPlanInfo] = []
    is_multi_floor: bool = False
    section_image_url: Optional[str] = None
    elevation_image_url: Optional[str] = None
    logs: List[str] = []
    error_message: Optional[str] = None
