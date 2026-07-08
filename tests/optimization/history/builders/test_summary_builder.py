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

    report = OptimizationReport(
        summary=ReportSummary(
            has_recommendations=True,
            total_strategies=2,
            total_recommendations=5,
            validated_recommendations=4,
            estimated_improvement_percent=81.5,
            highest_strategy_score=93.2,
        )
    )

    builder = SummaryBuilder()

    summary = builder.build(
        report,
    )

    assert summary.total_recommendations == 5

    assert summary.validated_recommendations == 4

    assert summary.total_strategies == 2

    assert summary.estimated_improvement_percent == 81.5

    assert summary.highest_strategy_score == 93.2