from __future__ import annotations

from dataclasses import dataclass, field

from backend.optimization.ranking.models.ranking import (
    Ranking,
)


@dataclass(slots=True)
class RankingResult:
    """
    Collection of ranked optimization recommendations.
    """

    rankings: list[Ranking] = field(
        default_factory=list,
    )

    def add(
        self,
        ranking: Ranking,
    ) -> None:

        self.rankings.append(
            ranking,
        )

    def sort(
        self,
    ) -> None:

        self.rankings.sort(
            key=lambda ranking: ranking.total_score,
            reverse=True,
        )