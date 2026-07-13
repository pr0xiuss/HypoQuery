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


class MemoryPolicyRepository(
    BasePolicyRepository,
):
    """
    In-memory repository used for testing
    and local execution.
    """

    def __init__(self) -> None:
        self._policies: dict[
            PolicyId,
            Policy,
        ] = {}

    def add(
        self,
        policy: Policy,
    ) -> None:
        self._policies[
            policy.id
        ] = policy

    def find(
        self,
        policy_id: PolicyId,
    ) -> Policy | None:
        return self._policies.get(
            policy_id,
        )

    def contains(
        self,
        policy_id: PolicyId,
    ) -> bool:
        return (
            policy_id
            in self._policies
        )