from __future__ import annotations

from backend.knowledge.models.enums import (
    KnowledgeNodeType,
)
from backend.knowledge.models.graph_snapshot import (
    GraphSnapshot,
)
from backend.knowledge.models.knowledge_node import (
    KnowledgeNode,
)
from backend.knowledge.retrieval.filters.node_filter import (
    NodeFilter,
)
from backend.knowledge.models.node_key import (
    NodeKey,
)

class GraphFilter:
    """
    High-level filtering operations over immutable
    GraphSnapshots.
    """

    def __init__(
        self,
        node_filter: NodeFilter,
    ) -> None:

        self._node_filter = node_filter

    def nodes_by_type(
        self,
        graph: GraphSnapshot,
        node_type: KnowledgeNodeType,
    ) -> tuple[
        KnowledgeNode,
        ...,
    ]:

        return self._node_filter.by_type(
            graph.nodes,
            node_type,
        )
    
    def neighbours(
        self,
        graph: GraphSnapshot,
        key: NodeKey,
    ) -> tuple[
        KnowledgeNode,
        ...,
    ]:

        neighbours: dict[
            NodeKey,
            KnowledgeNode,
        ] = {}

        node_lookup = {
            node.key: node
            for node in graph.nodes
        }

        for relationship in graph.relationships:

            if relationship.source == key:

                node = node_lookup.get(
                    relationship.target,
                )

                if node is not None:

                    neighbours[
                        node.key
                    ] = node

            elif relationship.target == key:

                node = node_lookup.get(
                    relationship.source,
                )

                if node is not None:

                    neighbours[
                        node.key
                    ] = node

        return tuple(
            neighbours.values(),
        )