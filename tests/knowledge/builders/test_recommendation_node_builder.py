from backend.knowledge.models.enums import KnowledgeNodeType
from backend.knowledge.projection.builders.recommendation_node_builder import (
    RecommendationNodeBuilder,
)
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


def test_build_recommendation_node() -> None:

    builder = RecommendationNodeBuilder()

    recommendation = Recommendation(
        category=RecommendationCategory.INDEX,
        code="CREATE_INDEX",
        key=RecommendationKey(
            category="index",
            target="users",
            action="create",
        ),
        title="Create Index",
        description="Create an index.",
        priority=RecommendationPriority.HIGH,
    )

    node = builder.build(recommendation)

    assert node.type == KnowledgeNodeType.RECOMMENDATION
    assert node.key.value == "recommendation:CREATE_INDEX"
    assert node.properties["code"] == "CREATE_INDEX"