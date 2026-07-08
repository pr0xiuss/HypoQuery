from __future__ import annotations

from collections.abc import Iterator

from backend.optimization.ranking.scorers.base_scorer import RankingScorer


class ScorerRegistry:
    """
    Registry of ranking scorers.
    """

    def __init__(
        self,
    ) -> None:

        self._scorers: list[
            RankingScorer
        ] = []

    def register(
        self,
        scorer: RankingScorer,
    ) -> None:

        self._scorers.append(
            scorer,
        )

    def __iter__(
        self,
    ) -> Iterator[
        RankingScorer
    ]:

        return iter(
            self._scorers,
        )

    def __len__(
        self,
    ) -> int:

        return len(
            self._scorers,
        )