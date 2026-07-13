from uuid import uuid4

from backend.operations.models.enums import (
    OptimizationHealthStatus,
    PolicyDecisionType,
)
from backend.operations.models.identifiers import (
    MonitoringId,
)
from backend.operations.monitoring.models.health import (
    OptimizationHealth,
)
from backend.operations.monitoring.models.summary import (
    MonitoringSummary,
)
from backend.operations.policy.composition import (
    PolicyComposition,
)
from backend.operations.policy.models.decision import (
    PolicyDecision,
)
from backend.operations.policy.models.rule import (
    PolicyRule,
)


def test_monitoring_to_policy() -> None:
    context = (
        PolicyComposition()
        .compose()
    )

    policy = context.service.create(
        monitoring=MonitoringSummary(
            id=MonitoringId(uuid4()),
            health=OptimizationHealth(
                status=OptimizationHealthStatus.DEGRADING,
                confidence=0.94,
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
            confidence=0.97,
            summary="Policy recommends reopening.",
        ),
    )

    assert (
        policy.decision.decision
        == PolicyDecisionType.REOPEN_CASE
    )