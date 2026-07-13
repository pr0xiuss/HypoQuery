from backend.operations.monitoring.builders.monitoring_builder import (
    MonitoringBuilder,
)
from backend.operations.monitoring.context import (
    MonitoringContext,
)
from backend.operations.monitoring.engine import (
    MonitoringEngine,
)
from backend.operations.monitoring.repositories.memory_repository import (
    MemoryMonitoringRepository,
)
from backend.operations.monitoring.service import (
    MonitoringService,
)


def test_context_creates_dependencies() -> None:
    context = MonitoringContext(
        repository=MemoryMonitoringRepository(),
    )

    assert isinstance(
        context.repository,
        MemoryMonitoringRepository,
    )

    assert isinstance(
        context.builder,
        MonitoringBuilder,
    )

    assert isinstance(
        context.engine,
        MonitoringEngine,
    )

    assert isinstance(
        context.service,
        MonitoringService,
    )