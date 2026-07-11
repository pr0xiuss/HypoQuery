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
from backend.knowledge.projection.builders.recommendation_relationship_builder import (
    RecommendationRelationshipBuilder,
)
from backend.optimization.recommendation.models.metadata import (
    RecommendationMetadata,
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


def test_build_recommendation_relationships():

    graph = KnowledgeGraph()

    graph.add_node(
        KnowledgeNode(
            key=NodeKey("finding:SEQ_SCAN"),
            type=KnowledgeNodeType.FINDING,
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
        description="Create an index.",
        priority=RecommendationPriority.HIGH,
        metadata=RecommendationMetadata(
            originating_findings=[
                "SEQ_SCAN",
            ],
        ),
    )

    builder = RecommendationRelationshipBuilder()

    relationships = builder.build(
        recommendation,
        graph,
    )

    assert len(relationships) == 1

    assert relationships[0].type == (
        KnowledgeRelationshipType.LEADS_TO
    )