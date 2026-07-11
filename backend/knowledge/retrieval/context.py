from __future__ import annotations

from dataclasses import dataclass, field

from backend.knowledge.retrieval.evidence.evidence_set import (
    EvidenceSet,
)
from backend.knowledge.retrieval.job import (
    RetrievalJob,
)
from backend.knowledge.models.node_key import (
    NodeKey,
)

@dataclass(slots=True)
class RetrievalContext:
    """
    Mutable state shared across the retrieval pipeline.

    Retrievers contribute evidence to the same
    EvidenceSet while satisfying one RetrievalObjective.
    """

    job: RetrievalJob

    evidence: EvidenceSet = field(
        default_factory=EvidenceSet,
    )

    visited: set[
        NodeKey
    ] = field(
        default_factory=set,
    )