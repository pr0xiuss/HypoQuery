from __future__ import annotations

from backend.knowledge.models.explanation import (
    Explanation,
)
from backend.knowledge.models.explanation_priority import (
    ExplanationPriority,
)
from backend.knowledge.models.explanation_section import (
    ExplanationSection,
)


class ExplanationFilter:
    """
    Filtering utilities operating on complete
    explanations.
    """

    def by_priority(
        self,
        explanation: Explanation,
        priority: ExplanationPriority,
    ) -> tuple[
        ExplanationSection,
        ...,
    ]:

        return tuple(
            section
            for section in explanation.sections
            if section.priority == priority
        )