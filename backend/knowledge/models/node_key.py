from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class NodeKey:
    """
    Immutable deterministic identity for a KnowledgeNode.

    A NodeKey uniquely identifies a knowledge entity across
    every projection and graph rebuild.

    Keys are domain-derived rather than randomly generated,
    ensuring stable graph topology over time.
    """

    value: str

    def __str__(self) -> str:
        return self.value