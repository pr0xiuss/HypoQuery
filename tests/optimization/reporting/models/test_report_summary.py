from backend.optimization.reporting.models.report_summary import (
    ReportSummary,
)


def test_report_summary():

    summary = ReportSummary(
        has_recommendations=True,
        total_strategies=2,
        total_recommendations=5,
        validated_recommendations=4,
        estimated_improvement_percent=72.5,
        highest_strategy_score=91.2,
    )

    assert summary.has_recommendations

    assert summary.total_strategies == 2

    assert summary.total_recommendations == 5

    assert summary.validated_recommendations == 4

    assert summary.estimated_improvement_percent == 72.5

    assert summary.highest_strategy_score == 91.2