from __future__ import annotations

from dataclasses import dataclass, field

from backend.knowledge.explanation_state.job import (
    ExplanationJob,
)
from backend.knowledge.models.explanation import (
    Explanation,
)


@dataclass(slots=True)
class ExplanationContext:
    """
    Mutable state shared across the explanation
    generation pipeline.

    Explainers collaborate to assemble a complete
    Explanation from an OptimizationContext.
    """

    job: ExplanationJob

    explanation: Explanation = field(
        default_factory=Explanation,
    )