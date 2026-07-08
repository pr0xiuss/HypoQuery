from __future__ import annotations

from dataclasses import dataclass

from backend.optimization.history.models.execution_record import (
    ExecutionRecord,
)


@dataclass(frozen=True, slots=True)
class ComparisonResult:
    """
    Result of comparing two execution records.
    """

    baseline: ExecutionRecord

    candidate: ExecutionRecord

    recommendation_delta: int

    validation_delta: int

    strategy_delta: int

    improvement_delta: float

    score_delta: float