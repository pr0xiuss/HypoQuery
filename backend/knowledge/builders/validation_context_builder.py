from __future__ import annotations

from backend.knowledge.builders.base_builder import (
    ContextBuilder,
)
from backend.knowledge.context import ContextContext
from backend.knowledge.models.context_priority import (
    ContextPriority,
)
from backend.knowledge.models.optimization_context import (
    OptimizationContext,
)
from backend.knowledge.retrieval.evidence.evidence_type import (
    EvidenceType,
)


class ValidationContextBuilder(ContextBuilder):
    """
    Builds validation sections from retrieved
    validation evidence.
    """

    def build(
        self,
        context: ContextContext,
        optimization_context: OptimizationContext,
    ) -> None:

        self._add_sections(
            context=context,
            optimization_context=optimization_context,
            evidence_type=EvidenceType.VALIDATION,
            title="Validation",
            priority=ContextPriority.SECONDARY,
        )