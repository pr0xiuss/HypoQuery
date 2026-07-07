from __future__ import annotations

from dataclasses import dataclass, field

from backend.optimization.reporting.models.recommendation_report import RecommendationReport
from backend.optimization.reporting.models.validation_report import ValidationReport
from backend.optimization.ranking.grouping.models.strategy_type import StrategyType


@dataclass(slots=True)
class StrategyReport:
    """
    Human-readable optimization strategy.
    """

    strategy: StrategyType

    overall_score: float

    representative: RecommendationReport

    validation: ValidationReport

    alternatives: list[
        RecommendationReport
    ] = field(
        default_factory=list,
    )