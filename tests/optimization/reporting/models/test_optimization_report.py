from backend.optimization.reporting.models.optimization_report import (
    OptimizationReport,
)
from backend.optimization.reporting.models.report_summary import (
    ReportSummary,
)


def test_optimization_report():

    summary = ReportSummary(
        has_recommendations=True,
        total_strategies=2,
        total_recommendations=4,
        validated_recommendations=3,
        estimated_improvement_percent=65,
        highest_strategy_score=91,
    )

    report = OptimizationReport(
        summary=summary,
    )

    assert report.summary == summary

    assert report.strategies == []

    assert report.generated_at is not None