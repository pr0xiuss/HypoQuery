from uuid import uuid4

from backend.operations.models.identifiers import (
    VerificationId,
)
from backend.operations.verification.models.summary import (
    VerificationSummary,
)


def test_verification_summary() -> None:
    summary = VerificationSummary(
        id=VerificationId(uuid4()),
        verified=True,
    )

    assert summary.verified