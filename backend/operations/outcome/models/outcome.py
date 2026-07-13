from __future__ import annotations

from dataclasses import dataclass

from backend.operations.models.identifiers import (
    OutcomeId,
)
from backend.operations.outcome.models.evidence import (
    OutcomeEvidence,
)
from backend.operations.outcome.models.metrics import (
    OutcomeMetrics,
)
from backend.operations.outcome.models.assessment import OutcomeAssessment

@dataclass(
    slots=True,
)
class Outcome:
    """
    Aggregate representing the engineering
    assessment of a verified optimization.
    """

    id: OutcomeId

    evidence: OutcomeEvidence

    metrics: OutcomeMetrics

    assessment: OutcomeAssessment