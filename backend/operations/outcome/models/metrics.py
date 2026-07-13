from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class OutcomeMetrics:
    """
    Quantitative metrics describing the
    engineering value of an optimization.
    """

    performance_improvement: float

    storage_overhead: float

    maintenance_cost: float