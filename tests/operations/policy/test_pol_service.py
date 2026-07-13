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
from backend.operations.policy.builders.policy_builder import (
    PolicyBuilder,
)
from backend.operations.policy.engine import (
    PolicyEngine,
)
from backend.operations.policy.models.decision import (
    PolicyDecision,
)
from backend.operations.policy.models.rule import (
    PolicyRule,
)
from backend.operations.policy.repositories.memory_repository import (
    MemoryPolicyRepository,
)
from backend.operations.policy.service import (
    PolicyService,
)


def test_service_creates_policy_snapshot() -> None:
    repository = MemoryPolicyRepository()

    service = PolicyService(
        engine=PolicyEngine(
            repository,
        ),
        builder=PolicyBuilder(),
    )

    snapshot = service.create(
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
            confidence=0.96,
            summary="Policy recommends reopening.",
        ),
    )

    assert (
        snapshot.decision.decision
        == PolicyDecisionType.REOPEN_CASE
    )