from __future__ import annotations

from collections.abc import Iterator

from backend.optimization.ranking.grouping.base_grouper import (
    StrategyGrouper,
)
from backend.optimization.ranking.grouping.models.strategy_type import (
    StrategyType,
)
from backend.optimization.ranking.models.ranking import (
    Ranking,
)


class StrategyRegistry:
    """
    Registry of strategy groupers.
    """

    def __init__(self,) -> None:

        self._groupers: list[
            StrategyGrouper
        ] = []

    def register(self, grouper: StrategyGrouper,) -> None:

        self._groupers.append(
            grouper,
        )

    def find_strategy_type(self, ranking: Ranking,) -> StrategyType:

        for grouper in self._groupers:

            strategy_type = grouper.classify(
                ranking,
            )

            if strategy_type is not None:

                return strategy_type

        raise LookupError(
            f"No strategy grouper registered "
            f"for recommendation "
            f"'{ranking.recommendation.code}'."
        )

    def __iter__(self,) -> Iterator[StrategyGrouper]:

        return iter(
            self._groupers,
        )

    def __len__(self,) -> int:

        return len(
            self._groupers,
        )