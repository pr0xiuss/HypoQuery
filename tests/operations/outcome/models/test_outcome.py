from uuid import uuid4

from backend.operations.models.identifiers import (
    OutcomeId,
    VerificationId,
)
from backend.operations.outcome.models.assessment import (
    OutcomeAssessment,
)
from backend.operations.outcome.models.evidence import (
    OutcomeEvidence,
)
from backend.operations.outcome.models.metrics import (
    OutcomeMetrics,
)
from backend.operations.outcome.models.outcome import (
    Outcome,
)
from backend.operations.verification.models.summary import (
    VerificationSummary,
)


def test_outcome() -> None:
    outcome = Outcome(
        id=OutcomeId(uuid4()),
        evidence=OutcomeEvidence(
            verification=VerificationSummary(
                id=VerificationId(uuid4()),
                verified=True,
            ),
            summary="Verification succeeded.",
        ),
        metrics=OutcomeMetrics(
            performance_improvement=72.0,
            storage_overhead=5.0,
            maintenance_cost=1.0,
        ),
        assessment=OutcomeAssessment(
            category="SUCCESSFUL",
            confidence=0.96,
            summary="Optimization produced significant gains.",
        ),
    )

    assert outcome.metrics.performance_improvement == 72.0
    assert outcome.assessment.category == "SUCCESSFUL"
    assert outcome.evidence.verification.verified