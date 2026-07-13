from __future__ import annotations

from backend.operations.cases.context import (
    CaseContext,
)
from backend.operations.cases.repositories.memory_repository import (
    MemoryCaseRepository,
)


class CaseComposition:
    """
    Composition root for the
    Optimization Case capability.
    """

    def compose(self) -> CaseContext:
        repository = MemoryCaseRepository()

        return CaseContext(
            repository=repository,
        )