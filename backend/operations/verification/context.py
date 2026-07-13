from __future__ import annotations

from backend.operations.verification.builders.verification_builder import (
    VerificationBuilder,
)
from backend.operations.verification.engine import (
    VerificationEngine,
)
from backend.operations.verification.repositories.base_repository import (
    BaseVerificationRepository,
)
from backend.operations.verification.service import (
    VerificationService,
)


class VerificationContext:
    """
    Runtime context for the
    Verification capability.
    """

    def __init__(
        self,
        repository: BaseVerificationRepository,
    ) -> None:
        self._repository = repository

        self._builder = VerificationBuilder()

        self._engine = VerificationEngine(
            repository=self._repository,
        )

        self._service = VerificationService(
            engine=self._engine,
            builder=self._builder,
        )

    @property
    def repository(self) -> BaseVerificationRepository:
        return self._repository

    @property
    def builder(self) -> VerificationBuilder:
        return self._builder

    @property
    def engine(self) -> VerificationEngine:
        return self._engine

    @property
    def service(self) -> VerificationService:
        return self._service