from uuid import uuid4

from backend.operations.contracts.snapshots import (
    VerificationSnapshot,
)
from backend.operations.integration.events.verification_events import (
    VerificationCompleted,
)
from backend.operations.models.identifiers import (
    VerificationId,
)


def test_verification_completed_event() -> None:
    snapshot = VerificationSnapshot(
        verification_id=VerificationId(uuid4()),
        verified=True,
    )

    event = VerificationCompleted(
        snapshot=snapshot,
    )

    assert event.snapshot == snapshot