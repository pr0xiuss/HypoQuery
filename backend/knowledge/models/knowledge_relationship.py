from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from backend.knowledge.models.enums import KnowledgeRelationshipType
from backend.knowledge.models.node_key import NodeKey
from backend.knowledge.models.relationship_key import RelationshipKey


@dataclass(slots=True)
class KnowledgeRelationship:
    """
    Represents a semantic relationship between two
    KnowledgeNodes.

    Relationships describe optimization knowledge,
    not graph storage details.
    """

    key: RelationshipKey

    type: KnowledgeRelationshipType

    source: NodeKey

    target: NodeKey

    properties: dict[str, Any] = field(
        default_factory=dict,
    )
