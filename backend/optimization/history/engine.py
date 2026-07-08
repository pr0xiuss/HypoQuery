from __future__ import annotations

from backend.optimization.history.builders.execution_record_builder import ExecutionRecordBuilder
from backend.optimization.history.context import HistoryContext
from backend.optimization.history.models.history_result import HistoryResult
from backend.optimization.history.repositories.execution_record_repository import ExecutionRecordRepository
from backend.optimization.history.comparison.comparison_engine import ComparisonEngine


class HistoryEngine:
    """
    Records completed optimization executions.
    """

    def __init__(
        self,
        record_builder: ExecutionRecordBuilder,
        repository: ExecutionRecordRepository,
        comparison_engine: ComparisonEngine,
    ) -> None:

        self._record_builder = record_builder

        self._repository = repository

        self._comparison_engine = comparison_engine

    def record(
        self,
        context: HistoryContext,
    ) -> HistoryResult:

        result = HistoryResult()

        record = self._record_builder.build(
            context.execution,
            context.report,
        )

        self._repository.save(
            record,
        )

        result.add(
            record,
        )

        return result