from __future__ import annotations
from backend.optimization.recommendation.models.recommendation_key import RecommendationKey
from backend.optimization.recommendation.context import RecommendationContext
from backend.optimization.recommendation.helpers.finding_lookup import FindingLookup
from backend.optimization.recommendation.models.category import RecommendationCategory
from backend.optimization.recommendation.models.location import RecommendationLocation
from backend.optimization.recommendation.models.metadata import RecommendationMetadata
from backend.optimization.recommendation.models.priority import RecommendationPriority
from backend.optimization.recommendation.models.recommendation import Recommendation
from backend.optimization.recommendation.models.recommendation_collection import RecommendationCollection
from backend.optimization.recommendation.rules.base_rule import RecommendationRule


class UpdateStatisticsRule(RecommendationRule):
    """
    Recommends updating table statistics when the planner's
    cardinality estimates appear inaccurate.
    """

    @property
    def name(self) -> str:
        return "update_statistics"

    def recommend(
        self,
        context: RecommendationContext,
    ) -> RecommendationCollection:

        recommendations = RecommendationCollection()

        findings = FindingLookup(context)

        mismatch = findings.get(
            "CARDINALITY_MISMATCH",
        )

        if mismatch is None:
            return recommendations

        recommendations.add(
            Recommendation(
                category=RecommendationCategory.STATISTICS,
                code="UPDATE_STATISTICS",
                key=RecommendationKey(
                    category="statistics",
                    target=mismatch.location.relation or "unknown",
                    action="analyze",
                ),
                title="Update Table Statistics",
                description=(
                    "Run ANALYZE to refresh planner statistics."
                ),
                priority=RecommendationPriority.HIGH,
                location=RecommendationLocation(
                    relation=mismatch.location.relation,
                    schema=mismatch.location.schema,
                ),
                metadata=RecommendationMetadata(
                    attributes=mismatch.metadata.attributes.copy(),
                ),
            )
        )

        return recommendations