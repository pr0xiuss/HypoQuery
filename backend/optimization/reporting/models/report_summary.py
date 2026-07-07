from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ReportSummary:
    """
    Executive summary of an optimization report.
    """

    has_recommendations: bool = False

    total_strategies: int = 0

    total_recommendations: int = 0

    validated_recommendations: int = 0

    estimated_improvement_percent: float = 0.0

    highest_strategy_score: float = 0.0