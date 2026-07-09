from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from backend.knowledge.models.node_key import (
    NodeKey,
)
from backend.knowledge.retrieval.evidence.evidence_source import (
    EvidenceSource,
)
from backend.knowledge.retrieval.evidence.evidence_type import (
    EvidenceType,
)


@dataclass(slots=True)
class Evidence:
    """
    Represents one piece of retrieved optimization evidence.

    Evidence is the canonical output of the retrieval
    engine and serves as the input to context building.
    """

    key: NodeKey

    type: EvidenceType

    source: EvidenceSource

    confidence: float = 1.0

    attributes: dict[str, Any] = field(
        default_factory=dict,
    )