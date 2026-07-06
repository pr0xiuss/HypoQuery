from __future__ import annotations

from abc import ABC, abstractmethod

from backend.optimization.ranking.grouping.models.strategy_type import (
    StrategyType,
)
from backend.optimization.ranking.models.ranking import (
    Ranking,
)


class StrategyGrouper(ABC):
    """
    Classifies rankings into optimization strategies.
    """

    @property
    @abstractmethod
    def name(self,) -> str:
        ...

    @abstractmethod
    def classify(self, ranking: Ranking,) -> StrategyType | None:
        """
        Returns the strategy type for the supplied
        ranking, or None if this grouper does not
        handle it.
        """
        ...