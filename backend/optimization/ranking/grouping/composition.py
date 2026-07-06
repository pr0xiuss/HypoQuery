from __future__ import annotations

from backend.optimization.ranking.grouping.engine import (
    StrategyEngine,
)
from backend.optimization.ranking.grouping.groupers.default_grouper import (
    DefaultStrategyGrouper,
)
from backend.optimization.ranking.grouping.registry import (
    StrategyRegistry,
)


def build_strategy_engine(
) -> StrategyEngine:
    """
    Builds the strategy grouping bounded context.
    """

    registry = StrategyRegistry()

    registry.register(
        DefaultStrategyGrouper(),
    )

    return StrategyEngine(
        registry,
    )