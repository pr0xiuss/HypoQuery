from uuid import uuid4

from backend.optimization.history.comparison.comparison_engine import (
    ComparisonEngine,
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


def create_record(
    recommendations: int,
    validations: int,
    strategies: int,
    improvement: float,
    score: float,
):

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
        summary=ExecutionSummary(
            total_recommendations=recommendations,
            validated_recommendations=validations,
            total_strategies=strategies,
            estimated_improvement_percent=improvement,
            highest_strategy_score=score,
        ),
        snapshot=OptimizationSnapshot(
            report=OptimizationReport(
                summary=ReportSummary(),
            ),
        ),
    )


def test_compare():

    engine = ComparisonEngine()

    baseline = create_record(
        recommendations=2,
        validations=1,
        strategies=1,
        improvement=40,
        score=60,
    )

    candidate = create_record(
        recommendations=5,
        validations=4,
        strategies=2,
        improvement=80,
        score=90,
    )

    result = engine.compare(
        baseline,
        candidate,
    )

    assert result.recommendation_delta == 3

    assert result.validation_delta == 3

    assert result.strategy_delta == 1

    assert result.improvement_delta == 40

    assert result.score_delta == 30