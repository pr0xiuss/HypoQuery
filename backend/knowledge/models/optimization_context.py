from __future__ import annotations

from dataclasses import dataclass, field

from backend.knowledge.models.context_section import (
    ContextSection,
)
from backend.knowledge.models.supporting_evidence import (
    SupportingEvidence,
)


@dataclass(slots=True)
class OptimizationContext:
    """
    Canonical reasoning context assembled from retrieved
    evidence.

    This object is the primary output of the Context
    Builder and serves as the input to the explanation
    layer.
    """

    sections: list[
        ContextSection,
    ] = field(
        default_factory=list,
    )

    supporting_evidence: list[
        SupportingEvidence,
    ] = field(
        default_factory=list,
    )

    def add_section(
        self,
        section: ContextSection,
    ) -> None:

        self.sections.append(
            section,
        )

    def add_supporting_evidence(
        self,
        evidence: SupportingEvidence,
    ) -> None:

        self.supporting_evidence.append(
            evidence,
        )