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


class MemoryOutcomeRepository(
    BaseOutcomeRepository,
):
    """
    In-memory repository used for testing
    and local execution.
    """

    def __init__(self) -> None:
        self._outcomes: dict[
            OutcomeId,
            Outcome,
        ] = {}

    def add(
        self,
        outcome: Outcome,
    ) -> None:
        self._outcomes[
            outcome.id
        ] = outcome

    def find(
        self,
        outcome_id: OutcomeId,
    ) -> Outcome | None:
        return self._outcomes.get(
            outcome_id,
        )

    def contains(
        self,
        outcome_id: OutcomeId,
    ) -> bool:
        return (
            outcome_id
            in self._outcomes
        )