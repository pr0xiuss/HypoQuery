from __future__ import annotations

from abc import ABC, abstractmethod

from backend.knowledge.explanation import (
    ExplanationContext,
)
from backend.knowledge.models.explanation import (
    Explanation,
)
from backend.knowledge.models.context_priority import (
    ContextPriority,
)
from backend.knowledge.models.explanation_priority import (
    ExplanationPriority,
)
from backend.knowledge.models.explanation_section import (
    ExplanationSection,
)


class Explainer(ABC):
    """
    Base contract implemented by every explanation
    builder.
    """

    @abstractmethod
    def explain(
        self,
        context: ExplanationContext,
        explanation: Explanation,
    ) -> None:
        """
        Contribute one or more sections to the
        Explanation.
        """

    def _add_sections(
        self,
        context: ExplanationContext,
        explanation: Explanation,
        title: str,
        context_priority: ContextPriority,
        explanation_priority: ExplanationPriority,
    ) -> None:
        """
        Copy matching context sections into the
        explanation.
        """

        for section in context.job.context.sections:

            if (
                section.priority
                != context_priority
            ):
                continue

            if (
                section.title
                != title
            ):
                continue

            explanation.add_section(
                ExplanationSection(
                    title=section.title,
                    priority=explanation_priority,
                    content=dict(
                        section.attributes,
                    ),
                )
            )