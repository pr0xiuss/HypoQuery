from __future__ import annotations

from backend.optimization.ranking.models.ranking_dimension import RankingDimension
from backend.optimization.ranking.models.score import Score


class RankingPolicy:
    """
    Calculates the final ranking score from
    individual dimension scores.
    """

    def __init__(self,) -> None:

        self._weights = {
            RankingDimension.IMPACT: 0.35,
            RankingDimension.VALIDATION: 0.30,
            RankingDimension.CONFIDENCE: 0.20,
            RankingDimension.RISK: 0.15,
        }

        total = sum(
            self._weights.values(),
        )

        if abs(total - 1.0) > 1e-9:

            raise ValueError(
                "Ranking weights must sum to 1.0."
            )

    def calculate(self, scores: list[Score],) -> float:

        total = 0.0

        for score in scores:

            total += (
                score.score
                * self._weights[
                    score.dimension
                ]
            )

        return total