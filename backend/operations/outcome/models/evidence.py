from __future__ import annotations

from dataclasses import dataclass

from backend.operations.verification.models.summary import (
    VerificationSummary,
)


@dataclass(
    frozen=True,
    slots=True,
)
class OutcomeEvidence:
    """
    Evidence supporting an operational outcome.
    """

    verification: VerificationSummary

    summary: str