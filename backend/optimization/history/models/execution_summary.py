from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ExecutionSummary:
    """
    High-level summary of an optimization execution.
    """

    total_recommendations: int = 0

    validated_recommendations: int = 0

    total_strategies: int = 0

    estimated_improvement_percent: float = 0.0

    highest_strategy_score: float = 0.0