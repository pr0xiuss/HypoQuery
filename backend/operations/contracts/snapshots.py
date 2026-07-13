from __future__ import annotations

from dataclasses import dataclass

from backend.operations.models.identifiers import (
    OptimizationCaseId,
)
from backend.operations.models.enums import (
    CasePriority,
    CaseStatus,
)
from backend.operations.models.identifiers import (
    VerificationId,
)
from backend.operations.models.identifiers import (
    OutcomeId,
)
from backend.operations.outcome.models.assessment import (
    OutcomeAssessment,
)
from backend.operations.models.identifiers import (
    MonitoringId,
)
from backend.operations.monitoring.models.health import (
    OptimizationHealth,
)
from backend.operations.models.identifiers import (
    PolicyId,
)
from backend.operations.policy.models.decision import (
    PolicyDecision,
)


@dataclass(
    frozen=True,
    slots=True,
)
class OptimizationCaseSnapshot:
    """
    Immutable public representation of an
    Optimization Case.
    """

    case_id: OptimizationCaseId

    status: CaseStatus

    priority: CasePriority

@dataclass(
    frozen=True,
    slots=True,
)
class VerificationSnapshot:
    """
    Published snapshot representing
    the result of a verification.
    """

    verification_id: VerificationId

    verified: bool

@dataclass(
    frozen=True,
    slots=True,
)
class OutcomeSnapshot:
    """
    Published snapshot representing
    an assessed optimization outcome.
    """

    outcome_id: OutcomeId

    assessment: OutcomeAssessment

@dataclass(
    frozen=True,
    slots=True,
)
class MonitoringSnapshot:
    """
    Published snapshot representing the
    current monitoring state.
    """

    monitoring_id: MonitoringId

    health: OptimizationHealth

@dataclass(
    frozen=True,
    slots=True,
)
class PolicySnapshot:
    """
    Published snapshot representing
    the result of policy evaluation.
    """

    policy_id: PolicyId

    decision: PolicyDecision