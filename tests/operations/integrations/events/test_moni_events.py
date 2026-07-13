from uuid import uuid4

from backend.operations.contracts.snapshots import (
    MonitoringSnapshot,
)
from backend.operations.integration.events.monitoring_events import (
    MonitoringUpdated,
)
from backend.operations.models.enums import (
    OptimizationHealthStatus,
)
from backend.operations.models.identifiers import (
    MonitoringId,
)
from backend.operations.monitoring.models.health import (
    OptimizationHealth,
)


def test_monitoring_updated_event() -> None:
    snapshot = MonitoringSnapshot(
        monitoring_id=MonitoringId(uuid4()),
        health=OptimizationHealth(
            status=OptimizationHealthStatus.HEALTHY,
            confidence=0.96,
            summary="Optimization healthy.",
        ),
    )

    event = MonitoringUpdated(
        snapshot=snapshot,
    )

    assert event.snapshot == snapshot