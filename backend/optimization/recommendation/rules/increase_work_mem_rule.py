from __future__ import annotations
from backend.optimization.recommendation.models.recommendation_key import RecommendationKey
from backend.optimization.recommendation.context import RecommendationContext
from backend.optimization.recommendation.helpers.finding_lookup import FindingLookup
from backend.optimization.recommendation.models.category import RecommendationCategory
from backend.optimization.recommendation.models.metadata import RecommendationMetadata
from backend.optimization.recommendation.models.priority import RecommendationPriority
from backend.optimization.recommendation.models.recommendation import Recommendation
from backend.optimization.recommendation.models.recommendation_collection import RecommendationCollection
from backend.optimization.recommendation.rules.base_rule import RecommendationRule


class IncreaseWorkMemRule(RecommendationRule):
    """
    Recommends increasing work_mem when disk spills occur
    during expensive sort operations.
    """

    @property
    def name(self) -> str:
        return "increase_work_mem"

    def recommend(
        self,
        context: RecommendationContext,
    ) -> RecommendationCollection:

        recommendations = RecommendationCollection()

        findings = FindingLookup(context)

        if not findings.has_all(
            "TEMP_DISK_WRITES",
            "EXPENSIVE_SORT",
        ):
            return recommendations

        recommendations.add(
            Recommendation(
                category=RecommendationCategory.CONFIGURATION,
                code="INCREASE_WORK_MEM",
                key=RecommendationKey(
                    category="configuration",
                    target="work_mem",
                    action="increase",
                ),
                title="Increase work_mem",
                description=(
                    "Consider increasing work_mem to reduce "
                    "temporary disk writes during sorting."
                ),
                priority=RecommendationPriority.MEDIUM,
                metadata=RecommendationMetadata(),
            )
        )

        return recommendations