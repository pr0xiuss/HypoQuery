from __future__ import annotations

from dataclasses import dataclass

from backend.knowledge.models.context_metadata import (
    ContextMetadata,
)
from backend.knowledge.models.context_section import (
    ContextSection,
)
from backend.knowledge.models.supporting_evidence import (
    SupportingEvidence,
)


@dataclass(frozen=True, slots=True)
class ContextSnapshot:
    """
    Immutable snapshot of an assembled
    OptimizationContext.

    Context snapshots are the canonical output
    of the Context Builder.
    """

    metadata: ContextMetadata

    sections: tuple[
        ContextSection,
        ...,
    ]

    supporting_evidence: tuple[
        SupportingEvidence,
        ...,
    ]