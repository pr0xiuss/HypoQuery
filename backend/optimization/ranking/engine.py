from __future__ import annotations

from backend.optimization.ranking.context import RankingContext
from backend.optimization.ranking.models.ranking import Ranking
from backend.optimization.ranking.models.ranking_result import RankingResult
from backend.optimization.ranking.policy import RankingPolicy
from backend.optimization.ranking.registry.scorer_registry import ScorerRegistry

from backend.optimization.validation.models.validation import Validation


class RankingEngine:
    """
    Coordinates execution of all ranking scorers.
    """

    def __init__(self, registry: ScorerRegistry, policy: RankingPolicy,) -> None:

        self._registry = registry

        self._policy = policy

    def rank(self, context: RankingContext,) -> RankingResult:

        result = RankingResult()

        validations = {
            validation.recommendation.key: validation
            for validation in context.validation_result.validations
        }

        for recommendation in (
            context.recommendation_result.recommendations
        ):

            validation = validations.get(
                recommendation.key,
            )

            scores = {}

            for scorer in self._registry:

                score = scorer.score(
                    context,
                    recommendation,
                    validation,
                )

                scores[
                    score.dimension
                ] = score

            ranking = Ranking(
                recommendation=recommendation,
                validation=validation,
                scores=scores,
                total_score=self._policy.calculate(
                    list(
                        scores.values(),
                    ),
                ),
            )

            result.add(
                ranking,
            )

        result.sort()

        return result