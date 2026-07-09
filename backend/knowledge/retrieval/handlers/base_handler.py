from __future__ import annotations

from abc import ABC, abstractmethod

from backend.knowledge.retrieval.context import (
    RetrievalContext,
)
from backend.knowledge.retrieval.evidence.evidence_set import (
    EvidenceSet,
)


class Retriever(ABC):
    """
    Base contract implemented by every deterministic
    knowledge retriever.
    """

    @abstractmethod
    def retrieve(
        self,
        context: RetrievalContext,
        evidence: EvidenceSet,
    ) -> None:
        """
        Contribute evidence for one retrieval objective.
        """