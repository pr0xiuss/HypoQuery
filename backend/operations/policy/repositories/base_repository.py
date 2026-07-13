from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from backend.operations.models.identifiers import (
    PolicyId,
)
from backend.operations.policy.models.policy import (
    Policy,
)


class BasePolicyRepository(ABC):
    """
    Repository contract for
    Policy aggregates.
    """

    @abstractmethod
    def add(
        self,
        policy: Policy,
    ) -> None:
        """
        Add a Policy aggregate.
        """

    @abstractmethod
    def find(
        self,
        policy_id: PolicyId,
    ) -> Policy | None:
        """
        Find a Policy aggregate.
        """

    @abstractmethod
    def contains(
        self,
        policy_id: PolicyId,
    ) -> bool:
        """
        Determine whether a Policy
        aggregate exists.
        """