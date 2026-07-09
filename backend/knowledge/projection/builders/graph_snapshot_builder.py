from __future__ import annotations

from backend.knowledge.models.graph_snapshot import GraphSnapshot
from backend.knowledge.models.knowledge_graph import KnowledgeGraph


class GraphSnapshotBuilder:
    """
    Freezes a mutable KnowledgeGraph into an immutable
    GraphSnapshot.

    GraphSnapshots are the published output of the
    Knowledge Projection subsystem.
    """

    def build(
        self,
        graph: KnowledgeGraph,
    ) -> GraphSnapshot:
        return GraphSnapshot(
            nodes=tuple(
                graph.nodes.values(),
            ),
            relationships=tuple(
                graph.relationships.values(),
            ),
        )