from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from backend.knowledge.models.knowledge_node import KnowledgeNode
from backend.knowledge.models.knowledge_relationship import (
    KnowledgeRelationship,
)


@dataclass(frozen=True, slots=True)
class GraphSnapshot:
    """
    Immutable snapshot of a projected Knowledge Graph.

    A GraphSnapshot represents the complete knowledge projection
    at a specific point in time and can be persisted, replayed,
    compared, or rebuilt.
    """

    nodes: tuple[KnowledgeNode, ...] = field(default_factory=tuple)

    relationships: tuple[KnowledgeRelationship, ...] = field(
        default_factory=tuple,
    )

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )