from __future__ import annotations

from backend.knowledge.retrieval.evidence.evidence_set import (
    EvidenceSet,
)


class EvidenceRanker:
    """
    Produces a deterministic ordering of retrieved
    evidence.
    """

    def rank(
        self,
        evidence: EvidenceSet,
    ) -> EvidenceSet:

        evidence.items.sort(
            key=lambda item: (
                -item.confidence,
                item.key.value,
            )
        )

        evidence.sort()
        return evidence