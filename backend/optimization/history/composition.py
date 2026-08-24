from __future__ import annotations

from backend.optimization.history.repositories.execution_record_repository import (
    ExecutionRecordRepository,
)
from backend.optimization.history.builders.execution_record_builder import (
    ExecutionRecordBuilder,
)
from backend.optimization.history.builders.snapshot_builder import (
    SnapshotBuilder,
)
from backend.optimization.history.builders.summary_builder import (
    SummaryBuilder,
)
from backend.optimization.history.engine import (
    HistoryEngine,
)
from backend.optimization.history.repositories.memory_repository import (
    MemoryExecutionRecordRepository,
)
from backend.optimization.history.comparison.comparison_engine import (
    ComparisonEngine,
)


def build_history_engine(
    repository: ExecutionRecordRepository | None = None,
) -> HistoryEngine:
    """
    Builds the History bounded context.
    """

    summary_builder = SummaryBuilder()

    snapshot_builder = SnapshotBuilder()

    record_builder = ExecutionRecordBuilder(
        summary_builder,
        snapshot_builder,
    )

    repository = repository or MemoryExecutionRecordRepository()

    comparison_engine = ComparisonEngine()

    return HistoryEngine(
        record_builder,
        repository,
        comparison_engine,
    )