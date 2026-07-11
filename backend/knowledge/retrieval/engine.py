from __future__ import annotations

from backend.knowledge.retrieval.context import (
    RetrievalContext,
)
from backend.knowledge.retrieval.evidence.evidence_set import (
    EvidenceSet,
)
from backend.knowledge.retrieval.registry.retrieval_registry import (
    RetrievalRegistry,
)


class RetrievalEngine:
    """
    Executes every registered retriever against one
    retrieval objective and builds an EvidenceSet.
    """

    def __init__(
        self,
        registry: RetrievalRegistry,
    ) -> None:

        self._registry = registry

    def retrieve(
        self,
        context: RetrievalContext,
    ) -> EvidenceSet:

        evidence = EvidenceSet()

        for retriever in self._registry.all():

            retriever.retrieve(
                context=context,
                evidence=evidence,
            )

        return evidence