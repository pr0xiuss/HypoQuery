from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ImprovementMetrics:
    """
    Quantifies the effect of applying a recommendation.
    """

    before_cost: float = 0.0

    after_cost: float = 0.0

    cost_delta: float = 0.0

    improvement_percent: float = 0.0

    before_rows: int = 0

    after_rows: int = 0

    plan_changed: bool = False

    cost_reduced: bool = False