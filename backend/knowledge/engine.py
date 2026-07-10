from __future__ import annotations

from backend.knowledge.context import (
    ContextContext,
)
from backend.knowledge.models.optimization_context import (
    OptimizationContext,
)
from backend.knowledge.registry.context_registry import (
    ContextRegistry,
)


class ContextEngine:
    """
    Executes every registered ContextBuilder and
    assembles an OptimizationContext.
    """

    def __init__(
        self,
        registry: ContextRegistry,
    ) -> None:

        self._registry = registry

    def build(
        self,
        context: ContextContext,
    ) -> OptimizationContext:

        optimization_context = OptimizationContext()

        for builder in self._registry.all():

            builder.build(
                context=context,
                optimization_context=optimization_context,
            )

        return optimization_context