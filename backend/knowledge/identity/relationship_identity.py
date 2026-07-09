from __future__ import annotations

from backend.knowledge.models.node_key import NodeKey
from backend.knowledge.models.relationship_key import (
    RelationshipKey,
)
from backend.knowledge.models.enums import (
    KnowledgeRelationshipType,
)


class RelationshipIdentity:
    """
    Generates deterministic identities for KnowledgeRelationships.

    Relationship identities are derived from the semantic
    relationship together with the connected nodes.
    """

    @staticmethod
    def create(
        relationship_type: KnowledgeRelationshipType,
        source: NodeKey,
        target: NodeKey,
    ) -> RelationshipKey:
        return RelationshipKey(
            value=(
                f"{relationship_type.value}:"
                f"{source.value}:"
                f"{target.value}"
            ),
        )