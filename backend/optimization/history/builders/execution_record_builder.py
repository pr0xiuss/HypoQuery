from __future__ import annotations

from backend.execution.contracts.execution import (
    PipelineExecution,
)
from backend.optimization.history.builders.snapshot_builder import (
    SnapshotBuilder,
)
from backend.optimization.history.builders.summary_builder import (
    SummaryBuilder,
)
from backend.optimization.history.models.execution_metadata import (
    ExecutionMetadata,
)
from backend.optimization.history.models.execution_record import (
    ExecutionRecord,
)
from backend.optimization.reporting.models.optimization_report import (
    OptimizationReport,
)


class ExecutionRecordBuilder:
    """
    Builds execution records from completed pipeline executions.
    """

    def __init__(
        self,
        summary_builder: SummaryBuilder,
        snapshot_builder: SnapshotBuilder,
    ) -> None:

        self._summary_builder = summary_builder

        self._snapshot_builder = snapshot_builder

    def build(
        self,
        execution: PipelineExecution,
        report: OptimizationReport,
    ) -> ExecutionRecord:

        context = execution.context

        metadata = ExecutionMetadata(
            execution_id=context.execution_id,
            trace_id=context.trace_id,
            fingerprint=execution.state.fingerprint,
            normalized_sql=execution.state.normalized_sql,
            pipeline_name=context.pipeline_name,
            pipeline_version=context.pipeline_version,
            database=context.database,
            schema=context.schema,
        )

        execution.state.report = report

        return ExecutionRecord(
            metadata=metadata,
            summary=self._summary_builder.build(
                report,
            ),
            snapshot=self._snapshot_builder.build(
                execution,
            ),
        )