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


class MemoryMonitoringRepository(
    BaseMonitoringRepository,
):
    """
    In-memory repository used for testing
    and local execution.
    """

    def __init__(self) -> None:
        self._monitoring: dict[
            MonitoringId,
            Monitoring,
        ] = {}

    def add(
        self,
        monitoring: Monitoring,
    ) -> None:
        self._monitoring[
            monitoring.id
        ] = monitoring

    def find(
        self,
        monitoring_id: MonitoringId,
    ) -> Monitoring | None:
        return self._monitoring.get(
            monitoring_id,
        )

    def contains(
        self,
        monitoring_id: MonitoringId,
    ) -> bool:
        return (
            monitoring_id
            in self._monitoring
        )