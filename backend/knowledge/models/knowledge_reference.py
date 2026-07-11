from __future__ import annotations

from dataclasses import dataclass

from backend.knowledge.models.node_key import NodeKey


@dataclass(frozen=True, slots=True)
class KnowledgeReference:
    """
    Immutable reference to a knowledge entity.

    KnowledgeReference is the only mechanism used to reference
    knowledge across bounded contexts.

    It avoids exposing graph internals while providing a stable,
    deterministic identity.
    """

    node_key: NodeKey