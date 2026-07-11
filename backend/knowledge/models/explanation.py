from __future__ import annotations

from dataclasses import dataclass, field

from backend.knowledge.models.explanation_section import (
    ExplanationSection,
)
from backend.knowledge.models.explanation_summary import (
    ExplanationSummary,
)


@dataclass(slots=True)
class Explanation:
    """
    Canonical explanation assembled from an
    OptimizationContext.

    This model is renderer-agnostic and becomes the
    primary input for the Prompt Layer.
    """

    summary: ExplanationSummary = field(
        default_factory=ExplanationSummary,
    )

    sections: list[
        ExplanationSection,
    ] = field(
        default_factory=list,
    )

    def add_section(
        self,
        section: ExplanationSection,
    ) -> None:

        self.sections.append(
            section,
        )