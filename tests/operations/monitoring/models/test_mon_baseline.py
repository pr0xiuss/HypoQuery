from backend.operations.monitoring.models.baseline import (
    MonitoringBaseline,
)


def test_monitoring_baseline() -> None:
    baseline = MonitoringBaseline(
        execution_time=120.5,
        shared_buffers=42.0,
        planning_time=5.2,
    )

    assert baseline.execution_time == 120.5
    assert baseline.shared_buffers == 42.0
    assert baseline.planning_time == 5.2