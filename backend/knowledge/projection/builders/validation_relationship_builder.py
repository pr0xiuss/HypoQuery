from __future__ import annotations

from backend.knowledge.models.knowledge_graph import (
    KnowledgeGraph,
)
from backend.knowledge.models.knowledge_relationship import (
    KnowledgeRelationship,
)
from backend.optimization.validation.models.validation import (
    Validation,
)


class ValidationRelationshipBuilder:
    """
    Validation currently terminates the deterministic
    optimization chain.

    It does not create outgoing semantic relationships.
    """

    def build(
        self,
        validation: Validation,
        graph: KnowledgeGraph,
    ) -> list[KnowledgeRelationship]:

        return []