from __future__ import annotations

from backend.knowledge.retrieval.evidence.evidence import (
    Evidence,
)
from backend.knowledge.retrieval.evidence.evidence_type import (
    EvidenceType,
)


class EvidenceFilter:
    """
    Deterministic filtering utilities for retrieved
    evidence.
    """

    def by_type(
        self,
        evidence: tuple[
            Evidence,
            ...,
        ],
        evidence_type: EvidenceType,
    ) -> tuple[
        Evidence,
        ...,
    ]:

        return tuple(
            item
            for item in evidence
            if item.type == evidence_type
        )