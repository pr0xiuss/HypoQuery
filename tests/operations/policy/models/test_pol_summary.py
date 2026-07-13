from uuid import uuid4

from backend.operations.models.enums import (
    PolicyDecisionType,
)
from backend.operations.models.identifiers import (
    PolicyId,
)
from backend.operations.policy.models.decision import (
    PolicyDecision,
)
from backend.operations.policy.models.summary import (
    PolicySummary,
)


def test_policy_summary() -> None:
    summary = PolicySummary(
        id=PolicyId(uuid4()),
        decision=PolicyDecision(
            decision=PolicyDecisionType.NO_ACTION,
            confidence=0.98,
            summary="No further action required.",
        ),
    )

    assert (
        summary.decision.decision
        == PolicyDecisionType.NO_ACTION
    )