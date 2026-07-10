from __future__ import annotations

from dataclasses import dataclass

from backend.knowledge.models.context_priority import (
    ContextPriority,
)


@dataclass(frozen=True, slots=True)
class SectionScore:
    """
    Represents the ranking score assigned to a
    ContextSection.
    """

    priority: ContextPriority

    score: float