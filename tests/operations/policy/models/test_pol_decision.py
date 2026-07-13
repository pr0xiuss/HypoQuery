from backend.operations.models.enums import (
    PolicyDecisionType,
)
from backend.operations.policy.models.decision import (
    PolicyDecision,
)


def test_policy_decision() -> None:
    decision = PolicyDecision(
        decision=PolicyDecisionType.REOPEN_CASE,
        confidence=0.94,
        summary="Performance degraded beyond threshold.",
    )

    assert (
        decision.decision
        == PolicyDecisionType.REOPEN_CASE
    )

    assert decision.confidence == 0.94

    assert (
        decision.summary
        == "Performance degraded beyond threshold."
    )