from __future__ import annotations

from backend.operations.models.identifiers import (
    MonitoringId,
)
from backend.operations.monitoring.models.monitoring import (
    Monitoring,
)
from backend.operations.monitoring.repositories.base_repository import (
    BaseMonitoringRepository,
)


class MonitoringEngine:
    """
    Domain engine responsible for
    Monitoring operations.
    """

    def __init__(
        self,
        repository: BaseMonitoringRepository,
    ) -> None:
        self._repository = repository

    def create(
        self,
        monitoring: Monitoring,
    ) -> None:
        self._repository.add(
            monitoring,
        )

    def find(
        self,
        monitoring_id: MonitoringId,
    ) -> Monitoring | None:
        return self._repository.find(
            monitoring_id,
        )

    def contains(
        self,
        monitoring_id: MonitoringId,
    ) -> bool:
        return self._repository.contains(
            monitoring_id,
        )