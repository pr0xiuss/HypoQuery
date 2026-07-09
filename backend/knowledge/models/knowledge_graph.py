from __future__ import annotations

from dataclasses import dataclass, field

from backend.knowledge.models.knowledge_node import KnowledgeNode
from backend.knowledge.models.knowledge_relationship import (
    KnowledgeRelationship,
)
from backend.knowledge.models.node_key import NodeKey
from backend.knowledge.models.relationship_key import (
    RelationshipKey,
)


@dataclass(slots=True)
class KnowledgeGraph:
    """
    Aggregate root representing the complete optimization
    knowledge graph.

    The graph owns topology.

    Nodes never own neighbours.
    Relationships never own the graph.

    This aggregate is the authoritative in-memory
    representation of projected optimization knowledge.
    """

    nodes: dict[NodeKey, KnowledgeNode] = field(
        default_factory=dict,
    )

    relationships: dict[
        RelationshipKey,
        KnowledgeRelationship,
    ] = field(
        default_factory=dict,
    )