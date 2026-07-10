from __future__ import annotations

from dataclasses import dataclass, field

from backend.knowledge.context_state.job import (
    ContextJob,
)
from backend.knowledge.models.optimization_context import (
    OptimizationContext,
)


@dataclass(slots=True)
class ContextContext:
    """
    Mutable state shared across the context building
    pipeline.

    Builders contribute sections and supporting evidence
    while assembling one OptimizationContext.
    """

    job: ContextJob

    context: OptimizationContext = field(
        default_factory=OptimizationContext,
    )