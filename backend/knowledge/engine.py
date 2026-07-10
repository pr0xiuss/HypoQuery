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
from backend.knowledge.explanation import (
    ExplanationContext,
)
from backend.knowledge.models.explanation import (
    Explanation,
)
from backend.knowledge.registry.explanation_registry import (
    ExplanationRegistry,
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
    
    
class ExplanationEngine:
    """
    Executes every registered Explainer and assembles
    a complete Explanation.
    """

    def __init__(
        self,
        registry: ExplanationRegistry,
    ) -> None:

        self._registry = registry

    def explain(
        self,
        context: ExplanationContext,
    ) -> Explanation:

        explanation = Explanation()

        for explainer in self._registry.all():

            explainer.explain(
                context=context,
                explanation=explanation,
            )

        return explanation