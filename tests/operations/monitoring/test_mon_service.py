from uuid import uuid4

from backend.operations.models.enums import (
    OptimizationHealthStatus,
)
from backend.operations.models.identifiers import (
    OutcomeId,
)
from backend.operations.monitoring.builders.monitoring_builder import (
    MonitoringBuilder,
)
from backend.operations.monitoring.engine import (
    MonitoringEngine,
)
from backend.operations.monitoring.models.baseline import (
    MonitoringBaseline,
)
from backend.operations.monitoring.models.finding import (
    MonitoringFinding,
)
from backend.operations.monitoring.models.health import (
    OptimizationHealth,
)
from backend.operations.monitoring.repositories.memory_repository import (
    MemoryMonitoringRepository,
)
from backend.operations.monitoring.service import (
    MonitoringService,
)
from backend.operations.outcome.models.assessment import (
    OutcomeAssessment,
)
from backend.operations.outcome.models.summary import (
    OutcomeSummary,
)


def test_service_creates_monitoring_snapshot() -> None:
    repository = MemoryMonitoringRepository()

    service = MonitoringService(
        engine=MonitoringEngine(
            repository,
        ),
        builder=MonitoringBuilder(),
    )

    snapshot = service.create(
        outcome=OutcomeSummary(
            id=OutcomeId(uuid4()),
            assessment=OutcomeAssessment(
                category="SUCCESSFUL",
                confidence=0.95,
                summary="Optimization successful.",
            ),
        ),
        baseline=MonitoringBaseline(
            execution_time=100.0,
            shared_buffers=50.0,
            planning_time=4.0,
        ),
        finding=MonitoringFinding(
            health=OptimizationHealth(
                status=OptimizationHealthStatus.HEALTHY,
                confidence=0.98,
                summary="Healthy.",
            ),
            regression_detected=False,
            confidence=0.99,
            summary="No regression.",
        ),
    )

    assert (
        snapshot.health.status
        == OptimizationHealthStatus.HEALTHY
    )