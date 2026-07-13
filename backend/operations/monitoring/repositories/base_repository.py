from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from backend.operations.models.identifiers import (
    MonitoringId,
)
from backend.operations.monitoring.models.monitoring import (
    Monitoring,
)


class BaseMonitoringRepository(ABC):
    """
    Repository contract for Monitoring
    aggregates.
    """

    @abstractmethod
    def add(
        self,
        monitoring: Monitoring,
    ) -> None:
        """
        Add a Monitoring aggregate.
        """

    @abstractmethod
    def find(
        self,
        monitoring_id: MonitoringId,
    ) -> Monitoring | None:
        """
        Find a Monitoring aggregate.
        """

    @abstractmethod
    def contains(
        self,
        monitoring_id: MonitoringId,
    ) -> bool:
        """
        Determine whether a Monitoring
        aggregate exists.
        """