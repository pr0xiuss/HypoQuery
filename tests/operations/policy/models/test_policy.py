from uuid import uuid4

from backend.operations.models.enums import (
    OptimizationHealthStatus,
    PolicyDecisionType,
)
from backend.operations.models.identifiers import (
    MonitoringId,
    PolicyId,
)
from backend.operations.monitoring.models.health import (
    OptimizationHealth,
)
from backend.operations.monitoring.models.summary import (
    MonitoringSummary,
)
from backend.operations.policy.models.decision import (
    PolicyDecision,
)
from backend.operations.policy.models.policy import (
    Policy,
)
from backend.operations.policy.models.rule import (
    PolicyRule,
)


def test_policy() -> None:
    policy = Policy(
        id=PolicyId(uuid4()),
        monitoring=MonitoringSummary(
            id=MonitoringId(uuid4()),
            health=OptimizationHealth(
                status=OptimizationHealthStatus.DEGRADING,
                confidence=0.93,
                summary="Performance degrading.",
            ),
        ),
        rule=PolicyRule(
            name="Regression Threshold",
            threshold=5.0,
            description="Reopen on degradation.",
        ),
        decision=PolicyDecision(
            decision=PolicyDecisionType.REOPEN_CASE,
            confidence=0.95,
            summary="Policy recommends reopening.",
        ),
    )

    assert (
        policy.decision.decision
        == PolicyDecisionType.REOPEN_CASE
    )

    assert (
        policy.monitoring.health.status
        == OptimizationHealthStatus.DEGRADING
    )