from backend.operations.models.enums import (
    OptimizationHealthStatus,
)
from backend.operations.monitoring.models.finding import (
    MonitoringFinding,
)
from backend.operations.monitoring.models.health import (
    OptimizationHealth,
)


def test_monitoring_finding() -> None:
    finding = MonitoringFinding(
        health=OptimizationHealth(
            status=OptimizationHealthStatus.HEALTHY,
            confidence=0.94,
            summary="Optimization is healthy.",
        ),
        regression_detected=False,
        confidence=0.97,
        summary="No regression detected.",
    )

    assert (
        finding.health.status
        == OptimizationHealthStatus.HEALTHY
    )

    assert not finding.regression_detected

    assert finding.confidence == 0.97

    assert (
        finding.summary
        == "No regression detected."
    )