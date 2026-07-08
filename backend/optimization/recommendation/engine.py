from __future__ import annotations

from backend.optimization.recommendation.context import (
    RecommendationContext,
)
from backend.optimization.recommendation.models.recommendation_result import (
    RecommendationResult,
)
from backend.optimization.recommendation.registry.rule_registry import (
    RecommendationRuleRegistry,
)


class RecommendationEngine:
    """
    Entry point into the Recommendation bounded context.

    Coordinates deterministic recommendation rules and
    aggregates their results into a RecommendationResult.
    """

    def __init__(
        self,
        registry: RecommendationRuleRegistry,
    ) -> None:

        self._registry = registry

    def recommend(
        self,
        context: RecommendationContext,
    ) -> RecommendationResult:

        result = RecommendationResult()

        for rule in self._registry:

            recommendations = rule.recommend(
                context,
            )

            result.recommendations.extend(
                recommendations,
            )

        return result