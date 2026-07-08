from __future__ import annotations

from backend.optimization.history.models.execution_summary import (
    ExecutionSummary,
)
from backend.optimization.reporting.models.optimization_report import (
    OptimizationReport,
)


class SummaryBuilder:
    """
    Builds execution summaries from optimization reports.
    """

    def build(
        self,
        report: OptimizationReport,
    ) -> ExecutionSummary:

        summary = report.summary

        return ExecutionSummary(
            total_recommendations=summary.total_recommendations,
            validated_recommendations=summary.validated_recommendations,
            total_strategies=summary.total_strategies,
            estimated_improvement_percent=(
                summary.estimated_improvement_percent
            ),
            highest_strategy_score=(
                summary.highest_strategy_score
            ),
        )