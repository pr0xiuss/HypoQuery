from __future__ import annotations

from backend.knowledge.models.context_priority import (
    ContextPriority,
)
from backend.knowledge.models.optimization_context import (
    OptimizationContext,
)


class ContextRanker:
    """
    Produces a deterministic ordering of context
    sections.
    """

    _ORDER = {
        ContextPriority.PRIMARY: 0,
        ContextPriority.SECONDARY: 1,
        ContextPriority.SUPPORTING: 2,
    }

    def rank(
        self,
        context: OptimizationContext,
    ) -> OptimizationContext:

        context.sections.sort(
            key=lambda section: (
                self._ORDER[
                    section.priority
                ],
                section.title,
            ),
        )

        return context