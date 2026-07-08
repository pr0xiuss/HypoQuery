from backend.optimization.recommendation.models.category import (
    RecommendationCategory,
)
from backend.optimization.recommendation.models.priority import (
    RecommendationPriority,
)
from backend.optimization.recommendation.models.recommendation import (
    Recommendation,
)
from backend.optimization.recommendation.models.recommendation_key import (
    RecommendationKey,
)
from backend.optimization.recommendation.models.recommendation_result import (
    RecommendationResult,
)


def test_total_recommendations():

    result = RecommendationResult()

    result.recommendations.add(
        Recommendation(
            category=RecommendationCategory.INDEX,
            code="CREATE_INDEX",
            key=RecommendationKey(
                category=RecommendationCategory.INDEX,
                target="customers",
                action="create",
            ),
            title="Create Index",
            description="Create an index.",
            priority=RecommendationPriority.HIGH,
        )
    )

    assert result.total_recommendations == 1