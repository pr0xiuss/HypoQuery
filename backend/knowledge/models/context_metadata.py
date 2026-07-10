from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(frozen=True, slots=True)
class ContextMetadata:
    """
    Immutable metadata describing one assembled
    OptimizationContext.
    """

    objective: str

    evidence_count: int

    section_count: int

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )