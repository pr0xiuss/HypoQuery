from uuid import uuid4

from backend.operations.contracts.snapshots import (
    MonitoringSnapshot,
    OptimizationCaseSnapshot,
    OutcomeSnapshot,
    PolicySnapshot,
    VerificationSnapshot,
)
from backend.operations.models.enums import (
    CasePriority,
    CaseStatus,
    OptimizationHealthStatus,
    PolicyDecisionType,
)
from backend.operations.models.identifiers import (
    MonitoringId,
    OptimizationCaseId,
    OutcomeId,
    PolicyId,
    VerificationId,
)
from backend.operations.monitoring.models.health import (
    OptimizationHealth,
)
from backend.operations.outcome.models.assessment import (
    OutcomeAssessment,
)
from backend.operations.policy.models.decision import (
    PolicyDecision,
)


def test_published_contracts() -> None:
    case = OptimizationCaseSnapshot(
        case_id=OptimizationCaseId(uuid4()),
        status=CaseStatus.OPEN,
        priority=CasePriority.HIGH,
    )

    verification = VerificationSnapshot(
        verification_id=VerificationId(uuid4()),
        verified=True,
    )

    outcome = OutcomeSnapshot(
        outcome_id=OutcomeId(uuid4()),
        assessment=OutcomeAssessment(
            category="SUCCESSFUL",
            confidence=0.95,
            summary="Optimization successful.",
        ),
    )

    monitoring = MonitoringSnapshot(
        monitoring_id=MonitoringId(uuid4()),
        health=OptimizationHealth(
            status=OptimizationHealthStatus.HEALTHY,
            confidence=0.98,
            summary="Healthy.",
        ),
    )

    policy = PolicySnapshot(
        policy_id=PolicyId(uuid4()),
        decision=PolicyDecision(
            decision=PolicyDecisionType.NO_ACTION,
            confidence=0.99,
            summary="No action required.",
        ),
    )

    assert case is not None
    assert verification is not None
    assert outcome is not None
    assert monitoring is not None
    assert policy is not None