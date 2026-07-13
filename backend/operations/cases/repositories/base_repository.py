from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from backend.operations.cases.models.optimization_case import (
    OptimizationCase,
)
from backend.operations.models.identifiers import (
    OptimizationCaseId,
)


class BaseCaseRepository(ABC):
    """
    Repository contract for Optimization Cases.
    """

    @abstractmethod
    def add(
        self,
        case: OptimizationCase,
    ) -> None:
        """
        Add an Optimization Case.
        """

    @abstractmethod
    def find(
        self,
        case_id: OptimizationCaseId,
    ) -> OptimizationCase | None:
        """
        Find an Optimization Case.
        """

    @abstractmethod
    def contains(
        self,
        case_id: OptimizationCaseId,
    ) -> bool:
        """
        Determine whether an Optimization Case exists.
        """