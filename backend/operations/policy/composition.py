from __future__ import annotations

from backend.operations.policy.context import (
    PolicyContext,
)
from backend.operations.policy.repositories.memory_repository import (
    MemoryPolicyRepository,
)


class PolicyComposition:
    """
    Composition root for the
    Policy capability.
    """

    def compose(
        self,
    ) -> PolicyContext:
        repository = MemoryPolicyRepository()

        return PolicyContext(
            repository=repository,
        )