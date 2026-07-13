from __future__ import annotations

from backend.operations.policy.builders.policy_builder import (
    PolicyBuilder,
)
from backend.operations.policy.engine import (
    PolicyEngine,
)
from backend.operations.policy.repositories.base_repository import (
    BasePolicyRepository,
)
from backend.operations.policy.service import (
    PolicyService,
)


class PolicyContext:
    """
    Runtime context for the
    Policy capability.
    """

    def __init__(
        self,
        repository: BasePolicyRepository,
    ) -> None:
        self._repository = repository

        self._builder = PolicyBuilder()

        self._engine = PolicyEngine(
            repository=self._repository,
        )

        self._service = PolicyService(
            engine=self._engine,
            builder=self._builder,
        )

    @property
    def repository(
        self,
    ) -> BasePolicyRepository:
        return self._repository

    @property
    def builder(
        self,
    ) -> PolicyBuilder:
        return self._builder

    @property
    def engine(
        self,
    ) -> PolicyEngine:
        return self._engine

    @property
    def service(
        self,
    ) -> PolicyService:
        return self._service