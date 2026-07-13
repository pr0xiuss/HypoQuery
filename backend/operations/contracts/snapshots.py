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