from uuid import uuid4

from backend.operations.models.enums import (
    OptimizationHealthStatus,
)
from backend.operations.models.identifiers import (
    MonitoringId,
    OutcomeId,
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
from backend.operations.monitoring.models.monitoring import (
    Monitoring,
)
from backend.operations.outcome.models.assessment import (
    OutcomeAssessment,
)
from backend.operations.outcome.models.summary import (
    OutcomeSummary,
)


def test_monitoring() -> None:
    monitoring = Monitoring(
        id=MonitoringId(uuid4()),
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
                confidence=0.97,
                summary="Healthy.",
            ),
            regression_detected=False,
            confidence=0.98,
            summary="No regression.",
        ),
    )

    assert monitoring.baseline.execution_time == 100.0

    assert (
        monitoring.finding.health.status
        == OptimizationHealthStatus.HEALTHY
    )