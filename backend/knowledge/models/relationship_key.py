from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RelationshipKey:
    """
    Immutable deterministic identity for a KnowledgeRelationship.

    Relationship keys uniquely identify semantic relationships
    between two deterministic knowledge nodes.

    Keys remain stable across graph rebuilds and projection
    replays.
    """

    value: str

    def __str__(self) -> str:
        return self.value