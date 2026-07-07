from __future__ import annotations

from backend.optimization.history.comparison.comparison_result import (
    ComparisonResult,
)
from backend.optimization.history.models.execution_record import (
    ExecutionRecord,
)


class ComparisonEngine:
    """
    Compares two optimization executions.
    """

    def compare(
        self,
        baseline: ExecutionRecord,
        candidate: ExecutionRecord,
    ) -> ComparisonResult:

        return ComparisonResult(
            baseline=baseline,
            candidate=candidate,
            recommendation_delta=(
                candidate.summary.total_recommendations
                - baseline.summary.total_recommendations
            ),
            validation_delta=(
                candidate.summary.validated_recommendations
                - baseline.summary.validated_recommendations
            ),
            strategy_delta=(
                candidate.summary.total_strategies
                - baseline.summary.total_strategies
            ),
            improvement_delta=(
                candidate.summary.estimated_improvement_percent
                - baseline.summary.estimated_improvement_percent
            ),
            score_delta=(
                candidate.summary.highest_strategy_score
                - baseline.summary.highest_strategy_score
            ),
        )