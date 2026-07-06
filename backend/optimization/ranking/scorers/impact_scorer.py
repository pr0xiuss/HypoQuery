from __future__ import annotations

from backend.optimization.ranking.context import RankingContext
from backend.optimization.ranking.models.score import Score
from backend.optimization.ranking.scorers.base_scorer import RankingScorer
from backend.optimization.recommendation.models.recommendation import Recommendation
from backend.optimization.validation.models.validation import Validation
from backend.optimization.ranking.models.ranking_dimension import RankingDimension

class ImpactScorer(RankingScorer):
    """
    Scores recommendations based on measured performance improvement.
    """

    @property
    def name(self,) -> str:

        return "impact"

    def score(
        self,
        context: RankingContext,
        recommendation: Recommendation,
        validation: Validation | None,
    ) -> Score:

        if (
            validation is None
            or validation.metrics is None
        ):

            return Score(
                dimension=RankingDimension.VALIDATION,
                score=0.0,
                reason="No validation metrics available.",
            )

        improvement = (
            validation.metrics.improvement_percent
        )

        return Score(
            dimension=RankingDimension.IMPACT,
            score=min(
                improvement,
                100.0,
            ),
            reason=(
                f"Estimated cost improved by "
                f"{improvement:.1f}%."
            ),
        )