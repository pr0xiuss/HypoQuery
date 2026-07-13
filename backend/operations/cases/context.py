from __future__ import annotations

from backend.operations.cases.builders.case_builder import (
    CaseBuilder,
)
from backend.operations.cases.engine import (
    CaseEngine,
)
from backend.operations.cases.repositories.base_repository import (
    BaseCaseRepository,
)
from backend.operations.cases.service import (
    CaseService,
)


class CaseContext:
    """
    Runtime context for the
    Optimization Case capability.
    """

    def __init__(
        self,
        repository: BaseCaseRepository,
    ) -> None:
        self._repository = repository

        self._builder = CaseBuilder()

        self._engine = CaseEngine(
            repository=self._repository,
        )

        self._service = CaseService(
            engine=self._engine,
            builder=self._builder,
        )

    @property
    def repository(self) -> BaseCaseRepository:
        return self._repository

    @property
    def builder(self) -> CaseBuilder:
        return self._builder

    @property
    def engine(self) -> CaseEngine:
        return self._engine

    @property
    def service(self) -> CaseService:
        return self._service