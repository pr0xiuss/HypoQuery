from __future__ import annotations

from dataclasses import dataclass, field

from backend.knowledge.models.knowledge_node import KnowledgeNode
from backend.knowledge.models.knowledge_relationship import (
    KnowledgeRelationship,
)


@dataclass(frozen=True, slots=True)
class ProjectionResult:
    """
    Immutable result produced by a Projector.

    Contains the knowledge artifacts that should be
    merged into the KnowledgeGraph.
    """

    nodes: tuple[KnowledgeNode, ...] = field(
        default_factory=tuple,
    )

    relationships: tuple[
        KnowledgeRelationship,
        ...
    ] = field(
        default_factory=tuple,
    )