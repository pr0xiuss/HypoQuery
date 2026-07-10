from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(frozen=True, slots=True)
class ExplanationMetadata:
    """
    Immutable metadata describing one generated
    Explanation.
    """

    objective: str

    section_count: int

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )