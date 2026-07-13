from uuid import uuid4

from backend.operations.models.enums import (
    OptimizationHealthStatus,
)
from backend.operations.models.identifiers import (
    OutcomeId,
)
from backend.operations.monitoring.composition import (
    MonitoringComposition,
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
from backend.operations.outcome.models.assessment import (
    OutcomeAssessment,
)
from backend.operations.outcome.models.summary import (
    OutcomeSummary,
)


def test_outcome_to_monitoring() -> None:
    context = (
        MonitoringComposition()
        .compose()
    )

    monitoring = context.service.create(
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
            shared_buffers=48.0,
            planning_time=3.5,
        ),
        finding=MonitoringFinding(
            health=OptimizationHealth(
                status=OptimizationHealthStatus.HEALTHY,
                confidence=0.98,
                summary="Optimization remains healthy.",
            ),
            regression_detected=False,
            confidence=0.99,
            summary="No regression detected.",
        ),
    )

    assert (
        monitoring.health.status
        == OptimizationHealthStatus.HEALTHY
    )