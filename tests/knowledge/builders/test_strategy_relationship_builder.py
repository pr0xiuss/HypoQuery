from backend.knowledge.models.enums import (
    KnowledgeNodeType,
    KnowledgeRelationshipType,
)
from backend.knowledge.models.knowledge_graph import (
    KnowledgeGraph,
)
from backend.knowledge.models.knowledge_node import (
    KnowledgeNode,
)
from backend.knowledge.models.node_key import (
    NodeKey,
)
from backend.knowledge.projection.builders.strategy_relationship_builder import (
    StrategyRelationshipBuilder,
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
from backend.optimization.recommendation.models.recommendation import (
    Recommendation,
)
from backend.optimization.recommendation.models.category import (
    RecommendationCategory,
)
from backend.optimization.recommendation.models.recommendation_key import (
    RecommendationKey,
)
from backend.optimization.recommendation.models.priority import (
    RecommendationPriority,
)


def test_strategy_relationship_builder():

    graph = KnowledgeGraph()

    graph.add_node(
        KnowledgeNode(
            key=NodeKey(
                "recommendation:CREATE_INDEX",
            ),
            type=KnowledgeNodeType.RECOMMENDATION,
        )
    )

    recommendation = Recommendation(
        category=RecommendationCategory.INDEX,
        code="CREATE_INDEX",
        key=RecommendationKey(
            category="index",
            target="users",
            action="create",
        ),
        title="Create Index",
        description="Create Index",
        priority=RecommendationPriority.HIGH,
    )

    ranking = Ranking(
        recommendation=recommendation,
        validation=None,
        scores={},
        total_score=10,
    )

    strategy = Strategy(
        strategy_type=StrategyType.INDEXING,
        representative=ranking,
    )

    builder = StrategyRelationshipBuilder()

    relationships = builder.build(
        strategy,
        graph,
    )

    assert len(relationships) == 1

    assert relationships[0].type == (
        KnowledgeRelationshipType.CONTAINS
    )