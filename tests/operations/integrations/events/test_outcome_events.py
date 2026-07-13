from uuid import uuid4

from backend.operations.contracts.snapshots import (
    OutcomeSnapshot,
)
from backend.operations.integration.events.outcome_events import (
    OutcomePublished,
)
from backend.operations.models.identifiers import (
    OutcomeId,
)
from backend.operations.outcome.models.assessment import (
    OutcomeAssessment,
)


def test_outcome_published_event() -> None:
    snapshot = OutcomeSnapshot(
        outcome_id=OutcomeId(uuid4()),
        assessment=OutcomeAssessment(
            category="SUCCESSFUL",
            confidence=0.95,
            summary="Optimization successful.",
        ),
    )

    event = OutcomePublished(
        snapshot=snapshot,
    )

    assert event.snapshot == snapshot