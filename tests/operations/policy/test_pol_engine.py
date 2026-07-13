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
from backend.operations.policy.engine import (
    PolicyEngine,
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
from backend.operations.policy.repositories.memory_repository import (
    MemoryPolicyRepository,
)


def build_policy() -> Policy:
    return Policy(
        id=PolicyId(uuid4()),
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


def test_engine_creates_policy() -> None:
    repository = MemoryPolicyRepository()

    engine = PolicyEngine(
        repository=repository,
    )

    policy = build_policy()

    engine.create(
        policy,
    )

    assert engine.contains(
        policy.id,
    )


def test_engine_finds_policy() -> None:
    repository = MemoryPolicyRepository()

    engine = PolicyEngine(
        repository=repository,
    )

    policy = build_policy()

    engine.create(
        policy,
    )

    assert (
        engine.find(
            policy.id,
        )
        == policy
    )