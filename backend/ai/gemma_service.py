"""
gemma_service.py - Architectural Semantic AI Service

Coordinates spatial semantic reasoning for floor plans using deterministic symbolic deduction
with extensibility for local/remote LLM vision reasoning.
"""

import json
import logging
from typing import Dict, Any
from backend.core.models import PlanSemanticInferenceResponse
from backend.ai.rule_engine import classify_rooms_symbolically

logger = logging.getLogger("renderize.ai.semantic")


class ArchitecturalSemanticService:
    """Provides high-fidelity spatial reasoning for architectural floor plans."""

    def __init__(self):
        self.model_loaded = True
        self.model_name = "renderize-spatial-reasoner-v1"

    def infer_plan_semantics(self, model_data: Dict[str, Any]) -> PlanSemanticInferenceResponse:
        """
        Infers room typologies, material assignments, and circulation rules
        from extracted geometric primitives and text annotations.
        """
        source = model_data.get("source_file", "unknown")
        logger.info(f"Inferring architectural semantics for: {source}")
        response = classify_rooms_symbolically(model_data)
        logger.info(f"Deducted typology: '{response.project_typology}' with {len(response.rooms)} functional zones.")
        return response


# Global singleton instance
gemma_ai = ArchitecturalSemanticService()
