from __future__ import annotations

from backend.operations.outcome.builders.outcome_builder import (
    OutcomeBuilder,
)
from backend.operations.outcome.engine import (
    OutcomeEngine,
)
from backend.operations.outcome.repositories.base_repository import (
    BaseOutcomeRepository,
)
from backend.operations.outcome.service import (
    OutcomeService,
)


class OutcomeContext:
    """
    Runtime context for the
    Outcome capability.
    """

    def __init__(
        self,
        repository: BaseOutcomeRepository,
    ) -> None:
        self._repository = repository

        self._builder = OutcomeBuilder()

        self._engine = OutcomeEngine(
            repository=self._repository,
        )

        self._service = OutcomeService(
            engine=self._engine,
            builder=self._builder,
        )

    @property
    def repository(self) -> BaseOutcomeRepository:
        return self._repository

    @property
    def builder(self) -> OutcomeBuilder:
        return self._builder

    @property
    def engine(self) -> OutcomeEngine:
        return self._engine

    @property
    def service(self) -> OutcomeService:
        return self._service