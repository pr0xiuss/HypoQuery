from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(frozen=True, slots=True,)
class Decision:
    """
    Represents an engineering decision taken
    during the lifecycle of an Optimization Case.
    """

    action: str

    actor: str

    reason: str | None = None

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )