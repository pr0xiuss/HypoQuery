from backend.operations.outcome.models.metrics import (
    OutcomeMetrics,
)


def test_outcome_metrics() -> None:
    metrics = OutcomeMetrics(
        performance_improvement=67.5,
        storage_overhead=8.0,
        maintenance_cost=2.5,
    )

    assert metrics.performance_improvement == 67.5
    assert metrics.storage_overhead == 8.0
    assert metrics.maintenance_cost == 2.5