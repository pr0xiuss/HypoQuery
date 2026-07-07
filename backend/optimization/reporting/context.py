from __future__ import annotations

from dataclasses import dataclass

from backend.optimization.ranking.grouping.models.strategy_result import (
    StrategyResult,
)


@dataclass(slots=True)
class ReportingContext:
    """
    Input required to generate an optimization report.
    """

    strategy_result: StrategyResult