from __future__ import annotations

from dataclasses import dataclass
from backend.operations.outcome.models.assessment import OutcomeAssessment
from backend.operations.models.identifiers import (
    OutcomeId,
)


@dataclass(
    frozen=True,
    slots=True,
)
class OutcomeSummary:
    """
    Lightweight summary of an
    operational outcome.
    """

    id: OutcomeId

    assessment: OutcomeAssessment