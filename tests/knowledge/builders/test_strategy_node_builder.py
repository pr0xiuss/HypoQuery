from backend.knowledge.models.enums import KnowledgeNodeType
from backend.knowledge.projection.builders.strategy_node_builder import (
    StrategyNodeBuilder,
)
from backend.optimization.ranking.grouping.models.strategy import (
    Strategy,
)
from backend.optimization.ranking.grouping.models.strategy_type import (
    StrategyType,
)
from backend.optimization.ranking.models.ranking import (
    Ranking,
)
from backend.optimization.ranking.models.score import (
    Score,
)
from backend.optimization.ranking.models.ranking_dimension import (
    RankingDimension,
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


def test_build_strategy_node() -> None:

    builder = StrategyNodeBuilder()

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

    ranking = Ranking(
        recommendation=recommendation,
        validation=None,
        scores={
            RankingDimension.IMPACT: Score(
                dimension=RankingDimension.IMPACT,
                score=10.0,
                reason="Test score",
            ),
        },
        total_score=10.0,
    )

    strategy = Strategy(
        strategy_type=StrategyType.INDEXING,
        representative=ranking,
    )

    node = builder.build(strategy)

    assert node.type == KnowledgeNodeType.STRATEGY
    assert node.properties["strategy_type"] == "INDEXING"
    assert node.properties["overall_score"] == 10.0