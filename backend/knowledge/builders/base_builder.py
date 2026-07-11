from __future__ import annotations

from abc import ABC, abstractmethod

from backend.knowledge.context import ContextContext

from backend.knowledge.models.context_priority import (
    ContextPriority,
)
from backend.knowledge.models.context_section import (
    ContextSection,
)
from backend.knowledge.models.optimization_context import (
    OptimizationContext,
)
from backend.knowledge.retrieval.evidence.evidence_type import (
    EvidenceType,
)


class ContextBuilder(ABC):
    """
    Base contract implemented by every optimization
    context builder.
    """

    @abstractmethod
    def build(
        self,
        context: ContextContext,
        optimization_context: OptimizationContext,
    ) -> None:
        """
        Contribute one or more sections to the
        OptimizationContext.
        """

    def _add_sections(
        self,
        context: ContextContext,
        optimization_context: OptimizationContext,
        evidence_type: EvidenceType,
        title: str,
        priority: ContextPriority,
    ) -> None:
        """
        Add context sections for every piece of evidence
        matching the requested evidence type.
        """

        for evidence in context.job.evidence:

            if evidence.type != evidence_type:
                continue

            optimization_context.add_section(
                ContextSection(
                    title=title,
                    priority=priority,
                    attributes={
                        "key": evidence.key.value,
                        "confidence": evidence.confidence,
                    },
                )
            )