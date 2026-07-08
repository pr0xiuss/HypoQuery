from uuid import uuid4

from backend.optimization.history.models.execution_metadata import (
    ExecutionMetadata,
)
from backend.optimization.history.models.execution_record import (
    ExecutionRecord,
)
from backend.optimization.history.models.execution_summary import (
    ExecutionSummary,
)
from backend.optimization.history.models.optimization_snapshot import (
    OptimizationSnapshot,
)
from backend.optimization.reporting.models.optimization_report import (
    OptimizationReport,
)
from backend.optimization.reporting.models.report_summary import (
    ReportSummary,
)


def test_execution_record():

    metadata = ExecutionMetadata(
        execution_id=uuid4(),
        trace_id=uuid4(),
        fingerprint="fp",
        normalized_sql="SELECT 1;",
        pipeline_name="optimization",
        pipeline_version="1.0",
        database="postgres",
        schema="public",
    )

    summary = ExecutionSummary()

    snapshot = OptimizationSnapshot(
        report=OptimizationReport(
            summary=ReportSummary(),
        )
    )

    record = ExecutionRecord(
        metadata=metadata,
        summary=summary,
        snapshot=snapshot,
    )

    assert record.metadata == metadata

    assert record.summary == summary

    assert record.snapshot == snapshot