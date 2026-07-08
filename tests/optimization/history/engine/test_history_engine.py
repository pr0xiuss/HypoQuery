from uuid import uuid4

from backend.execution.contracts.execution import (
    PipelineExecution,
)
from backend.execution.contracts.job import (
    PipelineJob,
)
from backend.execution.contracts.context import (
    PipelineContext,
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
from backend.optimization.history.comparison.comparison_engine import (
    ComparisonEngine,
)
from backend.optimization.history.context import (
    HistoryContext,
)
from backend.optimization.history.engine import (
    HistoryEngine,
)
from backend.optimization.history.repositories.memory_repository import (
    MemoryExecutionRecordRepository,
)
from backend.optimization.reporting.models.optimization_report import (
    OptimizationReport,
)
from backend.optimization.reporting.models.report_summary import (
    ReportSummary,
)


def test_record():

    execution_id = uuid4()

    trace_id = uuid4()

    execution = PipelineExecution(
        job=PipelineJob(
            source="pytest",
            pipeline_version="1.0",
            job_id=execution_id,
            trace_id=trace_id,
        ),
        context=PipelineContext(
            execution_id=execution_id,
            trace_id=trace_id,
            pipeline_name="optimization",
            pipeline_version="1.0",
            database="postgres",
            schema="public",
        ),
    )

    execution.state.fingerprint = "fp"

    execution.state.normalized_sql = (
        "SELECT 1;"
    )

    report = OptimizationReport(
        summary=ReportSummary(
            has_recommendations=True,
            total_recommendations=2,
            validated_recommendations=1,
            total_strategies=1,
            estimated_improvement_percent=80,
            highest_strategy_score=90,
        ),
    )

    repository = (
        MemoryExecutionRecordRepository()
    )

    engine = HistoryEngine(
        ExecutionRecordBuilder(
            SummaryBuilder(),
            SnapshotBuilder(),
        ),
        repository,
        ComparisonEngine(),
    )

    result = engine.record(
        HistoryContext(
            execution=execution,
            report=report,
        ),
    )

    assert result.total_records == 1

    assert repository.count() == 1

    assert (
        repository.exists(
            execution_id,
        )
    )