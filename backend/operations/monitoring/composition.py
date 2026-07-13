from __future__ import annotations

from backend.operations.monitoring.context import (
    MonitoringContext,
)
from backend.operations.monitoring.repositories.memory_repository import (
    MemoryMonitoringRepository,
)


class MonitoringComposition:
    """
    Composition root for the
    Monitoring capability.
    """

    def compose(
        self,
    ) -> MonitoringContext:
        repository = MemoryMonitoringRepository()

        return MonitoringContext(
            repository=repository,
        )