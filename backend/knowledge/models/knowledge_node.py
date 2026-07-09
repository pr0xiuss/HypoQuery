from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from backend.knowledge.models.enums import KnowledgeNodeType
from backend.knowledge.models.node_key import NodeKey


@dataclass(slots=True)
class KnowledgeNode:
    """
    Represents a single immutable knowledge entity within the
    Knowledge Graph.

    A KnowledgeNode owns only its identity and properties.

    Graph topology is owned by KnowledgeGraph and
    KnowledgeRelationship.
    """

    key: NodeKey

    type: KnowledgeNodeType

    properties: dict[str, Any] = field(
        default_factory=dict,
    )
