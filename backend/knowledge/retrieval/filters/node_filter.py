from __future__ import annotations

from backend.knowledge.models.knowledge_node import (
    KnowledgeNode,
)
from backend.knowledge.models.enums import (
    KnowledgeNodeType,
)


class NodeFilter:
    """
    Deterministic node filtering utilities.
    """

    def by_type(
        self,
        nodes: tuple[
            KnowledgeNode,
            ...,
        ],
        node_type: KnowledgeNodeType,
    ) -> tuple[
        KnowledgeNode,
        ...,
    ]:

        return tuple(
            node
            for node in nodes
            if node.type == node_type
        )