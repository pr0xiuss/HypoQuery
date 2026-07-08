from __future__ import annotations
from dataclasses import dataclass
from backend.optimization.recommendation.models.category import RecommendationCategory
from backend.optimization.recommendation.models.priority import RecommendationPriority

@dataclass(slots=True)
class RecommendationReport:
    """
    Human-readable representation of one optimization recommendation.
    """

    title: str

    description: str

    category: RecommendationCategory

    priority: RecommendationPriority

    confidence: float

    validated: bool