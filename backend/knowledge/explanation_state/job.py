from __future__ import annotations

from dataclasses import dataclass

from backend.knowledge.models.explanation import (
    Explanation,
)
from backend.knowledge.models.context_snapshot import (
    ContextSnapshot,
)


@dataclass(frozen=True, slots=True)
class ExplanationJob:
    """
    Represents one explanation generation request.

    An ExplanationJob transforms an OptimizationContext
    into a deterministic Explanation.
    """

    context: ContextSnapshot

    explanation: Explanation