from __future__ import annotations

from dataclasses import dataclass

from backend.operations.models.identifiers import (
    MonitoringId,
)
from backend.operations.monitoring.models.health import (
    OptimizationHealth,
)


@dataclass(
    frozen=True,
    slots=True,
)
class MonitoringSummary:
    """
    Lightweight summary of a
    Monitoring aggregate.
    """

    id: MonitoringId

    health: OptimizationHealth