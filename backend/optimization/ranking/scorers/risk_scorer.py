from __future__ import annotations

from backend.optimization.ranking.context import RankingContext
from backend.optimization.ranking.models.ranking_dimension import RankingDimension
from backend.optimization.ranking.models.score import Score
from backend.optimization.ranking.scorers.base_scorer import RankingScorer
from backend.optimization.recommendation.models.category import RecommendationCategory
from backend.optimization.recommendation.models.recommendation import Recommendation
from backend.optimization.validation.models.validation import Validation


class RiskScorer(RankingScorer):
    """
    Scores implementation risk.
    Lower risk receives a higher score.
    """

    @property
    def name(
        self,
    ) -> str:

        return "risk"

    def score(
        self,
        context: RankingContext,
        recommendation: Recommendation,
        validation: Validation | None,
    ) -> Score:

        if recommendation.category == RecommendationCategory.INDEX:

            return Score(
                dimension=RankingDimension.RISK,
                score=90.0,
                reason="Index creation is low risk.",
            )

        return Score(
            dimension=RankingDimension.RISK,
            score=50.0,
            reason="Moderate implementation risk.",
        )