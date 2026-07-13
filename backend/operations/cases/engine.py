from __future__ import annotations

from backend.operations.cases.models.optimization_case import (
    OptimizationCase,
)
from backend.operations.cases.repositories.base_repository import (
    BaseCaseRepository,
)
from backend.operations.models.identifiers import (
    OptimizationCaseId,
)


class CaseEngine:
    """
    Domain engine responsible for
    Optimization Case operations.
    """

    def __init__(
        self,
        repository: BaseCaseRepository,
    ) -> None:
        self._repository = repository

    def create(
        self,
        case: OptimizationCase,
    ) -> None:
        self._repository.add(
            case,
        )

    def find(
        self,
        case_id: OptimizationCaseId,
    ) -> OptimizationCase | None:
        return self._repository.find(
            case_id,
        )

    def contains(
        self,
        case_id: OptimizationCaseId,
    ) -> bool:
        return self._repository.contains(
            case_id,
        )