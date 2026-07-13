from uuid import uuid4

from backend.operations.models.identifiers import (
    VerificationId,
)
from backend.operations.outcome.composition import (
    OutcomeComposition,
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
from backend.operations.verification.models.summary import (
    VerificationSummary,
)


def test_verification_to_outcome() -> None:
    context = (
        OutcomeComposition()
        .compose()
    )

    outcome = context.service.create(
        evidence=OutcomeEvidence(
            verification=VerificationSummary(
                id=VerificationId(
                    uuid4(),
                ),
                verified=True,
            ),
            summary="Verification completed.",
        ),
        metrics=OutcomeMetrics(
            performance_improvement=42.0,
            storage_overhead=4.0,
            maintenance_cost=1.0,
        ),
        assessment=OutcomeAssessment(
            category="SUCCESSFUL",
            confidence=0.96,
            summary="Optimization succeeded.",
        ),
    )

    assert (
        outcome.assessment.category
        == "SUCCESSFUL"
    )