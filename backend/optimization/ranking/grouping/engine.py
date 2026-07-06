from __future__ import annotations

from backend.optimization.ranking.grouping.context import (
    StrategyContext,
)
from backend.optimization.ranking.grouping.models.strategy import (
    Strategy,
)
from backend.optimization.ranking.grouping.models.strategy_result import (
    StrategyResult,
)
from backend.optimization.ranking.grouping.registry import (
    StrategyRegistry,
)


class StrategyEngine:
    """
    Groups ranked recommendations into optimization strategies.
    """

    def __init__(
        self,
        registry: StrategyRegistry,
    ) -> None:

        self._registry = registry

    def group(
        self,
        context: StrategyContext,
    ) -> StrategyResult:

        result = StrategyResult()

        for ranking in context.ranking_result.rankings:

            strategy_type = (
                self._registry.find_strategy_type(
                    ranking,
                )
            )

            strategy = result.get(
                strategy_type,
            )

            if strategy is None:

                result.add(
                    Strategy(
                        strategy_type=strategy_type,
                        representative=ranking,
                    )
                )

                continue

            strategy.add_alternative(
                ranking,
            )

        result.sort()

        return result