from __future__ import annotations

from backend.operations.models.identifiers import (
    OutcomeId,
)
from backend.operations.outcome.models.outcome import (
    Outcome,
)
from backend.operations.outcome.repositories.base_repository import (
    BaseOutcomeRepository,
)


class OutcomeEngine:
    """
    Domain engine responsible for
    Outcome operations.
    """

    def __init__(
        self,
        repository: BaseOutcomeRepository,
    ) -> None:
        self._repository = repository

    def create(
        self,
        outcome: Outcome,
    ) -> None:
        self._repository.add(
            outcome,
        )

    def find(
        self,
        outcome_id: OutcomeId,
    ) -> Outcome | None:
        return self._repository.find(
            outcome_id,
        )

    def contains(
        self,
        outcome_id: OutcomeId,
    ) -> bool:
        return self._repository.contains(
            outcome_id,
        )