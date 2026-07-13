from __future__ import annotations

from dataclasses import dataclass

from backend.operations.models.enums import (
    CasePriority,
    CaseStatus,
)
from backend.operations.models.identifiers import (
    OptimizationCaseId,
)


@dataclass(
    frozen=True,
    slots=True,
)
class CaseSummary:
    """
    Lightweight representation of an
    Optimization Case used by repositories
    and read models.
    """

    id: OptimizationCaseId

    status: CaseStatus

    priority: CasePriority

    total_recommendations: int