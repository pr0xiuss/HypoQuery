from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from backend.operations.models.identifiers import (
    OutcomeId,
)
from backend.operations.outcome.models.outcome import (
    Outcome,
)


class BaseOutcomeRepository(ABC):
    """
    Repository contract for Outcome aggregates.
    """

    @abstractmethod
    def add(
        self,
        outcome: Outcome,
    ) -> None:
        """
        Add an Outcome.
        """

    @abstractmethod
    def find(
        self,
        outcome_id: OutcomeId,
    ) -> Outcome | None:
        """
        Find an Outcome.
        """

    @abstractmethod
    def contains(
        self,
        outcome_id: OutcomeId,
    ) -> bool:
        """
        Determine whether an Outcome exists.
        """