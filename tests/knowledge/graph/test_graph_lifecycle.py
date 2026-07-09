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


def test_graph_lifecycle():

    graph = KnowledgeGraph()

    node = KnowledgeNode(
        key=NodeKey("node"),
        type=KnowledgeNodeType.QUERY,
    )

    graph.add_node(
        node,
    )

    assert graph.node_count() == 1

    copied = graph.copy()

    assert copied.node_count() == 1

    graph.remove_node(
        node.key,
    )

    assert graph.node_count() == 0

    graph.add_node(
        node,
    )

    graph.clear()

    assert graph.is_empty()