from __future__ import annotations

from backend.knowledge.models.explanation_priority import (
    ExplanationPriority,
)
from backend.knowledge.models.explanation_section import (
    ExplanationSection,
)


class SectionFilter:
    """
    Deterministic filtering utilities for
    ExplanationSections.
    """

    def by_priority(
        self,
        sections: tuple[
            ExplanationSection,
            ...,
        ],
        priority: ExplanationPriority,
    ) -> tuple[
        ExplanationSection,
        ...,
    ]:

        return tuple(
            section
            for section in sections
            if section.priority == priority
        )