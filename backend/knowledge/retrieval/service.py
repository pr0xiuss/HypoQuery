from __future__ import annotations

from backend.knowledge.retrieval.context import (
    RetrievalContext,
)
from backend.knowledge.retrieval.engine import (
    RetrievalEngine,
)
from backend.knowledge.retrieval.evidence.evidence_set import (
    EvidenceSet,
)


class RetrievalService:
    """
    Application service responsible for executing the
    complete retrieval pipeline.

    RetrievalObjective
            ↓
      RetrievalEngine
            ↓
        EvidenceSet
    """

    def __init__(
        self,
        engine: RetrievalEngine,
    ) -> None:

        self._engine = engine

    def retrieve(
        self,
        context: RetrievalContext,
    ) -> EvidenceSet:

        return self._engine.retrieve(
            context=context,
        )