from backend.optimization.history.models.execution_summary import (
    ExecutionSummary,
)


def test_execution_summary():

    summary = ExecutionSummary(
        total_recommendations=5,
        validated_recommendations=4,
        total_strategies=2,
        estimated_improvement_percent=82.5,
        highest_strategy_score=93.1,
    )

    assert summary.total_recommendations == 5

    assert summary.validated_recommendations == 4

    assert summary.total_strategies == 2

    assert summary.estimated_improvement_percent == 82.5

    assert summary.highest_strategy_score == 93.1