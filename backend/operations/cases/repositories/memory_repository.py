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


class MemoryCaseRepository(
    BaseCaseRepository,
):
    """
    In-memory repository used for testing
    and local execution.
    """

    def __init__(self) -> None:
        self._cases: dict[
            OptimizationCaseId,
            OptimizationCase,
        ] = {}

    def add(
        self,
        case: OptimizationCase,
    ) -> None:
        self._cases[
            case.id
        ] = case

    def find(
        self,
        case_id: OptimizationCaseId,
    ) -> OptimizationCase | None:
        return self._cases.get(
            case_id,
        )

    def contains(
        self,
        case_id: OptimizationCaseId,
    ) -> bool:
        return case_id in self._cases