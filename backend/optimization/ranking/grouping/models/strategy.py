from __future__ import annotations

from dataclasses import dataclass, field

from backend.optimization.ranking.grouping.models.strategy_type import (
    StrategyType,
)
from backend.optimization.ranking.models.ranking import (
    Ranking,
)


@dataclass(slots=True)
class Strategy:
    """
    Represents one optimization strategy together with
    its alternative recommendations.
    """

    strategy_type: StrategyType

    representative: Ranking

    alternatives: list[
        Ranking
    ] = field(
        default_factory=list,
    )

    @property
    def overall_score(self,) -> float:

        return self.representative.total_score
    

    def add_alternative(self, ranking: Ranking,) -> None:

        if ranking == self.representative:
            return

        self.alternatives.append(
            ranking,
        )