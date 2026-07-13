from uuid import uuid4

import pytest

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
from backend.operations.policy.builders.policy_builder import (
    PolicyBuilder,
)
from backend.operations.policy.models.decision import (
    PolicyDecision,
)
from backend.operations.policy.models.rule import (
    PolicyRule,
)


def build_monitoring() -> MonitoringSummary:
    return MonitoringSummary(
        id=MonitoringId(uuid4()),
        health=OptimizationHealth(
            status=OptimizationHealthStatus.HEALTHY,
            confidence=0.96,
            summary="Optimization healthy.",
        ),
    )


def test_builder_builds_policy() -> None:
    policy = (
        PolicyBuilder()
        .with_id(
            PolicyId(uuid4()),
        )
        .with_monitoring(
            build_monitoring(),
        )
        .with_rule(
            PolicyRule(
                name="Regression Threshold",
                threshold=5.0,
                description="Reopen on degradation.",
            ),
        )
        .with_decision(
            PolicyDecision(
                decision=PolicyDecisionType.NO_ACTION,
                confidence=0.97,
                summary="Continue operation.",
            ),
        )
        .build()
    )

    assert (
        policy.decision.decision
        == PolicyDecisionType.NO_ACTION
    )


def test_builder_requires_identifier() -> None:
    builder = (
        PolicyBuilder()
        .with_monitoring(
            build_monitoring(),
        )
        .with_rule(
            PolicyRule(
                name="Regression Threshold",
                threshold=5.0,
                description="Reopen on degradation.",
            ),
        )
        .with_decision(
            PolicyDecision(
                decision=PolicyDecisionType.NO_ACTION,
                confidence=0.97,
                summary="Continue operation.",
            ),
        )
    )

    with pytest.raises(
        ValueError,
    ):
        builder.build()