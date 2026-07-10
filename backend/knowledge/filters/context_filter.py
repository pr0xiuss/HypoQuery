from __future__ import annotations

from backend.knowledge.models.context_priority import (
    ContextPriority,
)
from backend.knowledge.models.context_section import (
    ContextSection,
)


class ContextFilter:
    """
    Deterministic filtering utilities for context
    sections.
    """

    def by_priority(
        self,
        sections: tuple[
            ContextSection,
            ...,
        ],
        priority: ContextPriority,
    ) -> tuple[
        ContextSection,
        ...,
    ]:

        return tuple(
            section
            for section in sections
            if section.priority == priority
        )