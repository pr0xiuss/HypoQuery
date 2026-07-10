from __future__ import annotations

from backend.knowledge.builders.base_builder import (
    ContextBuilder,
)
import backend.knowledge.context_state
from backend.knowledge.models.context_priority import (
    ContextPriority,
)
from backend.knowledge.models.optimization_context import (
    OptimizationContext,
)
from backend.knowledge.retrieval.evidence.evidence_type import (
    EvidenceType,
)


class FindingContextBuilder(ContextBuilder):
    """
    Builds finding sections from retrieved
    finding evidence.
    """

    def build(
        self,
        context: backend.knowledge.context_state.ContextContext,
        optimization_context: OptimizationContext,
    ) -> None:

        self._add_sections(
            context=context,
            optimization_context=optimization_context,
            evidence_type=EvidenceType.FINDING,
            title="Finding",
            priority=ContextPriority.PRIMARY,
        )