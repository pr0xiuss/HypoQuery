from __future__ import annotations

from backend.operations.models.identifiers import (
    PolicyId,
)
from backend.operations.policy.models.policy import (
    Policy,
)
from backend.operations.policy.repositories.base_repository import (
    BasePolicyRepository,
)


class PolicyEngine:
    """
    Domain engine responsible for
    Policy operations.
    """

    def __init__(
        self,
        repository: BasePolicyRepository,
    ) -> None:
        self._repository = repository

    def create(
        self,
        policy: Policy,
    ) -> None:
        self._repository.add(
            policy,
        )

    def find(
        self,
        policy_id: PolicyId,
    ) -> Policy | None:
        return self._repository.find(
            policy_id,
        )

    def contains(
        self,
        policy_id: PolicyId,
    ) -> bool:
        return self._repository.contains(
            policy_id,
        )