from uuid import uuid4

from backend.operations.models.identifiers import (
    VerificationId,
)
from backend.operations.outcome.models.evidence import (
    OutcomeEvidence,
)
from backend.operations.verification.models.summary import (
    VerificationSummary,
)


def test_outcome_evidence() -> None:
    evidence = OutcomeEvidence(
        verification=VerificationSummary(
            id=VerificationId(uuid4()),
            verified=True,
        ),
        summary="Verification completed successfully.",
    )

    assert evidence.verification.verified

    assert (
        evidence.summary
        == "Verification completed successfully."
    )