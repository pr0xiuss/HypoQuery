from uuid import uuid4

from backend.operations.contracts.snapshots import (
    PolicySnapshot,
)
from backend.operations.integration.events.policy_events import (
    PolicyEvaluated,
)
from backend.operations.models.enums import (
    PolicyDecisionType,
)
from backend.operations.models.identifiers import (
    PolicyId,
)
from backend.operations.policy.models.decision import (
    PolicyDecision,
)


def test_policy_evaluated_event() -> None:
    snapshot = PolicySnapshot(
        policy_id=PolicyId(uuid4()),
        decision=PolicyDecision(
            decision=PolicyDecisionType.NO_ACTION,
            confidence=0.98,
            summary="No further action required.",
        ),
    )

    event = PolicyEvaluated(
        snapshot=snapshot,
    )

    assert event.snapshot == snapshot