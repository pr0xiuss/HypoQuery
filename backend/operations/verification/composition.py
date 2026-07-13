from __future__ import annotations

from backend.operations.verification.context import (
    VerificationContext,
)
from backend.operations.verification.repositories.memory_repository import (
    MemoryVerificationRepository,
)


class VerificationComposition:
    """
    Composition root for the
    Verification capability.
    """

    def compose(
        self,
    ) -> VerificationContext:
        repository = MemoryVerificationRepository()

        return VerificationContext(
            repository=repository,
        )