from __future__ import annotations

from dataclasses import dataclass

from backend.operations.models.identifiers import (
    VerificationId,
)


@dataclass(
    frozen=True,
    slots=True,
)
class VerificationSummary:
    """
    Lightweight summary of a completed
    verification.
    """

    id: VerificationId

    verified: bool