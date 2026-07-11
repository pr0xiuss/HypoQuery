from __future__ import annotations

from backend.knowledge.models.enums import (
    KnowledgeRelationshipType,
)
from backend.knowledge.models.knowledge_relationship import (
    KnowledgeRelationship,
)


class RelationshipFilter:
    """
    Deterministic relationship filtering utilities.
    """

    def by_type(
        self,
        relationships: tuple[
            KnowledgeRelationship,
            ...,
        ],
        relationship_type: KnowledgeRelationshipType,
    ) -> tuple[
        KnowledgeRelationship,
        ...,
    ]:

        return tuple(
            relationship
            for relationship in relationships
            if relationship.type == relationship_type
        )