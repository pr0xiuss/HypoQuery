from __future__ import annotations

from dataclasses import dataclass

from backend.execution.contracts.fingerprint import (
    QueryFingerprint,
)
from backend.optimization.recommendation.models.recommendation_result import (
    RecommendationResult,
)
from backend.optimization.validation.models.validation_result import (
    ValidationResult,
)


@dataclass(slots=True, frozen=True)
class RankingContext:
    """
    Input required by the ranking engine.
    """

    recommendation_result: RecommendationResult

    validation_result: ValidationResult

    fingerprint: QueryFingerprint | None