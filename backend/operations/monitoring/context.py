from __future__ import annotations

from backend.operations.monitoring.builders.monitoring_builder import (
    MonitoringBuilder,
)
from backend.operations.monitoring.engine import (
    MonitoringEngine,
)
from backend.operations.monitoring.repositories.base_repository import (
    BaseMonitoringRepository,
)
from backend.operations.monitoring.service import (
    MonitoringService,
)


class MonitoringContext:
    """
    Runtime context for the
    Monitoring capability.
    """

    def __init__(
        self,
        repository: BaseMonitoringRepository,
    ) -> None:
        self._repository = repository

        self._builder = MonitoringBuilder()

        self._engine = MonitoringEngine(
            repository=self._repository,
        )

        self._service = MonitoringService(
            engine=self._engine,
            builder=self._builder,
        )

    @property
    def repository(
        self,
    ) -> BaseMonitoringRepository:
        return self._repository

    @property
    def builder(
        self,
    ) -> MonitoringBuilder:
        return self._builder

    @property
    def engine(
        self,
    ) -> MonitoringEngine:
        return self._engine

    @property
    def service(
        self,
    ) -> MonitoringService:
        return self._service