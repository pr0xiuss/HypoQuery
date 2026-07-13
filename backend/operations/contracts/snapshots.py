from __future__ import annotations

from dataclasses import dataclass

from backend.operations.models.identifiers import (
    OptimizationCaseId,
)
from backend.operations.models.enums import (
    CasePriority,
    CaseStatus,
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