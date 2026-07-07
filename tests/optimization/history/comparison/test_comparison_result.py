from uuid import uuid4

from backend.optimization.history.comparison.comparison_result import (
    ComparisonResult,
)
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


def create_record():

    return ExecutionRecord(
        metadata=ExecutionMetadata(
            execution_id=uuid4(),
            trace_id=uuid4(),
            fingerprint="fp",
            normalized_sql="SELECT 1;",
            pipeline_name="optimization",
            pipeline_version="1.0",
            database="postgres",
            schema="public",
        ),
        summary=ExecutionSummary(),
        snapshot=OptimizationSnapshot(
            report=OptimizationReport(
                summary=ReportSummary(),
            ),
        ),
    )


def test_comparison_result():

    baseline = create_record()

    candidate = create_record()

    result = ComparisonResult(
        baseline=baseline,
        candidate=candidate,
        recommendation_delta=1,
        validation_delta=2,
        strategy_delta=3,
        improvement_delta=10.5,
        score_delta=5.2,
    )

    assert result.baseline == baseline

    assert result.candidate == candidate

    assert result.recommendation_delta == 1

    assert result.validation_delta == 2

    assert result.strategy_delta == 3

    assert result.improvement_delta == 10.5

    assert result.score_delta == 5.2