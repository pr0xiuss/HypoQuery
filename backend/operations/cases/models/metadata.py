from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from backend.operations.models.enums import (
    CaseIntent,
)


@dataclass(frozen=True, slots=True,)
class CaseMetadata:
    """
    Metadata associated with an
    Optimization Case.
    """

    intent: CaseIntent

    labels: list[str] = field(
        default_factory=list,
    )

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )

    updated_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )