from uuid import uuid4

from backend.operations.models.enums import (
    OptimizationHealthStatus,
)
from backend.operations.models.identifiers import (
    MonitoringId,
)
from backend.operations.monitoring.models.health import (
    OptimizationHealth,
)
from backend.operations.monitoring.models.summary import (
    MonitoringSummary,
)


def test_monitoring_summary() -> None:
    summary = MonitoringSummary(
        id=MonitoringId(uuid4()),
        health=OptimizationHealth(
            status=OptimizationHealthStatus.HEALTHY,
            confidence=0.96,
            summary="Healthy.",
        ),
    )

    assert (
        summary.health.status
        == OptimizationHealthStatus.HEALTHY
    )