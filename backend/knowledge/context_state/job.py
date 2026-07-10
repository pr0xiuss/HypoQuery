from __future__ import annotations

from dataclasses import dataclass

from backend.knowledge.retrieval.evidence.evidence_set import (
    EvidenceSet,
)
from backend.knowledge.retrieval.objectives.retrieval_objective import (
    RetrievalObjective,
)


@dataclass(frozen=True, slots=True)
class ContextJob:
    """
    Represents one context construction request.

    A ContextJob transforms retrieved evidence into an
    OptimizationContext for a specific retrieval objective.
    """

    objective: RetrievalObjective

    evidence: EvidenceSet