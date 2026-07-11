from backend.knowledge.models.enums import (
    KnowledgeNodeType,
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


def test_graph_queries():

    graph = KnowledgeGraph()

    graph.add_node(
        KnowledgeNode(
            key=NodeKey("finding"),
            type=KnowledgeNodeType.FINDING,
        )
    )

    graph.add_node(
        KnowledgeNode(
            key=NodeKey("recommendation"),
            type=KnowledgeNodeType.RECOMMENDATION,
        )
    )

    assert len(
        graph.nodes_by_type(
            KnowledgeNodeType.FINDING,
        )
    ) == 1

    assert len(
        graph.nodes_by_type(
            KnowledgeNodeType.RECOMMENDATION,
        )
    ) == 1

    assert graph.node_count() == 2

    assert graph.relationship_count() == 0