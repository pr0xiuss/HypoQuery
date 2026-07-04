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


class CreateIndexRule(RecommendationRule):
    """
    Recommends creating an index for expensive sequential scans.
    """

    @property
    def name(self) -> str:
        return "create_index"

    def recommend(
        self,
        context: RecommendationContext,
    ) -> RecommendationCollection:

        recommendations = RecommendationCollection()

        findings = FindingLookup(
            context,
        )

        scan = findings.get(
            "LARGE_TABLE_SCAN",
        )

        if scan is None:
            return recommendations

        recommendations.add(
            Recommendation(
                category=RecommendationCategory.INDEX,
                code="CREATE_INDEX",
                key=RecommendationKey(
                    category="index",
                    target=scan.location.relation or "unknown",
                    action="create",
                ),
                title="Create Index",
                description=(
                    "Consider creating an index to reduce "
                    "large sequential scans."
                ),
                priority=RecommendationPriority.HIGH,
                location=RecommendationLocation(
                    relation=scan.location.relation,
                    schema=scan.location.schema,
                ),
                metadata=RecommendationMetadata(
                    attributes=scan.metadata.attributes.copy(),
                ),
            )
        )

        return recommendations