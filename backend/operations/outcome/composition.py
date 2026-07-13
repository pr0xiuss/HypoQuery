from __future__ import annotations

from backend.operations.outcome.context import (
    OutcomeContext,
)
from backend.operations.outcome.repositories.memory_repository import (
    MemoryOutcomeRepository,
)


class OutcomeComposition:
    """
    Composition root for the
    Outcome capability.
    """

    def compose(
        self,
    ) -> OutcomeContext:
        repository = MemoryOutcomeRepository()

        return OutcomeContext(
            repository=repository,
        )