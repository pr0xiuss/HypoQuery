from backend.operations.monitoring.composition import (
    MonitoringComposition,
)
from backend.operations.monitoring.context import (
    MonitoringContext,
)


def test_monitoring_composition_creates_context() -> None:
    composition = MonitoringComposition()

    context = composition.compose()

    assert isinstance(
        context,
        MonitoringContext,
    )