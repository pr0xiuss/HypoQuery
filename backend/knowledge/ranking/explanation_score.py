from __future__ import annotations

from dataclasses import dataclass

from backend.knowledge.models.explanation_priority import (
    ExplanationPriority,
)


@dataclass(frozen=True, slots=True)
class ExplanationScore:
    """
    Represents the ranking score assigned to an
    ExplanationSection.
    """

    priority: ExplanationPriority

    score: float