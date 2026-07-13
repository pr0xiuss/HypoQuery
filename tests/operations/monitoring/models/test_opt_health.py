from backend.operations.models.enums import (
    OptimizationHealthStatus,
)
from backend.operations.monitoring.models.health import (
    OptimizationHealth,
)


def test_optimization_health() -> None:
    health = OptimizationHealth(
        status=OptimizationHealthStatus.HEALTHY,
        confidence=0.95,
        summary="Optimization remains healthy.",
    )

    assert (
        health.status
        == OptimizationHealthStatus.HEALTHY
    )

    assert health.confidence == 0.95

    assert (
        health.summary
        == "Optimization remains healthy."
    )