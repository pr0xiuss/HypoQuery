from __future__ import annotations

from backend.knowledge.explainers.base_explainer import (
    Explainer,
)
from backend.knowledge.explanation import (
    ExplanationContext,
)
from backend.knowledge.models.context_priority import (
    ContextPriority,
)
from backend.knowledge.models.explanation import (
    Explanation,
)
from backend.knowledge.models.explanation_priority import (
    ExplanationPriority,
)
from backend.knowledge.models.explanation_section import (
    ExplanationSection,
)


class ValidationExplainer(Explainer):
    """
    Converts validation context into explanation
    sections.
    """

    def explain(
        self,
        context: ExplanationContext,
        explanation: Explanation,
    ) -> None:

            self._add_sections(
                context=context,
                explanation=explanation,
                title="Validation",
                context_priority=ContextPriority.SECONDARY,
                explanation_priority=ExplanationPriority.SECONDARY,
            )