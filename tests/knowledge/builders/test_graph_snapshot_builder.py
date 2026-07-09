from backend.knowledge.models.graph_snapshot import GraphSnapshot
from backend.knowledge.models.knowledge_graph import (
    KnowledgeGraph,
)
from backend.knowledge.models.knowledge_node import (
    KnowledgeNode,
)
from backend.knowledge.models.enums import (
    KnowledgeNodeType,
)
from backend.knowledge.models.node_key import (
    NodeKey,
)
from backend.knowledge.projection.builders.graph_snapshot_builder import (
    GraphSnapshotBuilder,
)


def test_build_graph_snapshot() -> None:

    graph = KnowledgeGraph()

    node = KnowledgeNode(
        key=NodeKey("finding:SEQ_SCAN"),
        type=KnowledgeNodeType.FINDING,
    )

    graph.nodes[node.key] = node

    builder = GraphSnapshotBuilder()

    snapshot = builder.build(
        graph,
    )

    assert isinstance(
        snapshot,
        GraphSnapshot,
    )

    assert len(snapshot.nodes) == 1
    assert snapshot.nodes[0] == node