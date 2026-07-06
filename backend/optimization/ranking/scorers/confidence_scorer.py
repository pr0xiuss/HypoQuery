from __future__ import annotations

from backend.optimization.ranking.context import RankingContext
from backend.optimization.ranking.models.ranking_dimension import RankingDimension
from backend.optimization.ranking.models.score import Score
from backend.optimization.ranking.scorers.base_scorer import RankingScorer
from backend.optimization.recommendation.models.priority import RecommendationPriority
from backend.optimization.recommendation.models.recommendation import Recommendation
from backend.optimization.validation.models.validation import Validation
from backend.optimization.validation.models.validation_status import ValidationStatus


class ConfidenceScorer(RankingScorer):
    """
    Scores confidence in a recommendation.
    """

    @property
    def name(
        self,
    ) -> str:

        return "confidence"

    def score(
        self,
        context: RankingContext,
        recommendation: Recommendation,
        validation: Validation | None,
    ) -> Score:

        score = 50.0

        reason = "Rule-based recommendation."

        if recommendation.priority == RecommendationPriority.HIGH:
            score += 20
            reason = "High-priority rule."

        if (
            validation is not None
            and validation.status == ValidationStatus.VALIDATED
        ):
            score += 30
            reason = (
                "Recommendation validated using HypoPG."
            )

        return Score(
            dimension=RankingDimension.CONFIDENCE,
            score=min(score, 100.0),
            reason=reason,
        )