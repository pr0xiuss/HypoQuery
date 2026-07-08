from __future__ import annotations

from backend.optimization.ranking.context import RankingContext
from backend.optimization.ranking.models.score import Score
from backend.optimization.ranking.scorers.base_scorer import RankingScorer
from backend.optimization.recommendation.models.recommendation import Recommendation
from backend.optimization.validation.models.validation import Validation
from backend.optimization.validation.models.validation_status import ValidationStatus
from backend.optimization.ranking.models.ranking_dimension import RankingDimension

class ValidationScorer(RankingScorer):
    """
    Scores recommendations based on validation outcome.
    """

    @property
    def name(
        self,
    ) -> str:

        return "validation"

    def score(
        self,
        context: RankingContext,
        recommendation: Recommendation,
        validation: Validation | None,
    ) -> Score:

        if validation is None:

            return Score(
                dimension=RankingDimension.VALIDATION,
                score=0.0,
                reason="Recommendation has not been validated.",
            )

        if validation.status == ValidationStatus.VALIDATED:

            return Score(
                dimension=RankingDimension.VALIDATION,
                score=100.0,
                reason="Recommendation validated successfully.",
            )

        if validation.status == ValidationStatus.REJECTED:

            return Score(
                dimension=RankingDimension.VALIDATION,
                score=20.0,
                reason="Validation did not improve the execution plan.",
            )

        return Score(
            dimension=RankingDimension.VALIDATION,
            score=0.0,
            reason="Validation failed.",
        )