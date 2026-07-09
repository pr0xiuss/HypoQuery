from __future__ import annotations

from abc import ABC, abstractmethod

from backend.knowledge.models.knowledge_relationship import (
    KnowledgeRelationship,
)


class RelationshipBuilder(ABC):
    """
    Base contract for every semantic relationship builder.

    A RelationshipBuilder derives semantic relationships
    from a deterministic optimization artifact.
    """

    @abstractmethod
    def build(
        self,
        source: object,
    ) -> tuple[KnowledgeRelationship, ...]:
        """
        Build semantic relationships.
        """
        raise NotImplementedError