from uuid import uuid4

from backend.execution.contracts.context import PipelineContext
from backend.execution.contracts.execution import PipelineExecution
from backend.execution.contracts.job import PipelineJob
from backend.optimization.history.builders.execution_record_builder import (
    ExecutionRecordBuilder,
)
from backend.optimization.history.builders.snapshot_builder import (
    SnapshotBuilder,
)
from backend.optimization.history.builders.summary_builder import (
    SummaryBuilder,
)
from backend.optimization.reporting.models.optimization_report import (
    OptimizationReport,
)
from backend.optimization.reporting.models.report_summary import (
    ReportSummary,
)


def test_build():

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
    execution.state.normalized_sql = "SELECT 1;"

    report = OptimizationReport(
        summary=ReportSummary(
            total_recommendations=2,
            validated_recommendations=1,
            total_strategies=1,
            estimated_improvement_percent=75,
            highest_strategy_score=90,
        )
    )

    execution.state.report = report

    builder = ExecutionRecordBuilder(
        SummaryBuilder(),
        SnapshotBuilder(),
    )

    record = builder.build(
        execution,
        report,
    )

    assert record.metadata.execution_id == execution_id
    assert record.metadata.fingerprint == "fp"
    assert record.metadata.normalized_sql == "SELECT 1;"

    assert record.summary.total_recommendations == 2
    assert record.summary.validated_recommendations == 1
    assert record.summary.total_strategies == 1
    assert record.summary.estimated_improvement_percent == 75
    assert record.summary.highest_strategy_score == 90

    assert record.snapshot.summary == report.summary
    assert record.snapshot.findings == ()
    assert record.snapshot.recommendations == ()
    assert record.snapshot.validations == ()
    assert record.snapshot.strategies == ()