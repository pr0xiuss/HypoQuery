from __future__ import annotations

from dataclasses import dataclass, field

from backend.optimization.ranking.grouping.models.strategy import (
    Strategy,
)
from backend.optimization.ranking.grouping.models.strategy_type import (
    StrategyType,
)


@dataclass(slots=True)
class StrategyResult:
    """
    Collection of optimization strategies.
    """

    _strategies: dict[StrategyType, Strategy,] = field(default_factory=dict,)

    @property
    def strategies(self,) -> list[Strategy]:

        return list(
            self._strategies.values(),
        )
    

    def add(self, strategy: Strategy,) -> None:

        if strategy.strategy_type in self._strategies:

            raise ValueError(
                f"Strategy '{strategy.strategy_type.value}' already exists."
            )

        self._strategies[
            strategy.strategy_type
        ] = strategy


    def get(self, strategy_type: StrategyType,) -> Strategy | None:

        return self._strategies.get(
            strategy_type,
        )


    def sort(self,) -> None:

        ordered = sorted(
            self._strategies.values(),
            key=lambda strategy: strategy.overall_score,
            reverse=True,
        )

        self._strategies = {
            strategy.strategy_type: strategy
            for strategy in ordered
        }