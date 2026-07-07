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
from backend.optimization.history.models.history_result import (
    HistoryResult,
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


def test_history_result():

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

    record = ExecutionRecord(
        metadata=metadata,
        summary=ExecutionSummary(),
        snapshot=OptimizationSnapshot(
            report=OptimizationReport(
                summary=ReportSummary(),
            )
        ),
    )

    result = HistoryResult()

    result.add(
        record,
    )

    assert result.total_records == 1

    assert result.records[0] == record