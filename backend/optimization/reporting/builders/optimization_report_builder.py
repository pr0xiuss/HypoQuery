from __future__ import annotations

from backend.optimization.ranking.grouping.models.strategy_result import (
    StrategyResult,
)
from backend.optimization.reporting.builders.strategy_report_builder import (
    StrategyReportBuilder,
)
from backend.optimization.reporting.models.optimization_report import (
    OptimizationReport,
)
from backend.optimization.reporting.models.report_summary import (
    ReportSummary,
)


class OptimizationReportBuilder:
    """
    Builds the published optimization report.
    """

    def __init__(
        self,
        strategy_builder: StrategyReportBuilder,
    ) -> None:

        self._strategy_builder = (
            strategy_builder
        )

    def build(
        self,
        result: StrategyResult,
    ) -> OptimizationReport:

        reports = [
            self._strategy_builder.build(
                strategy,
            )
            for strategy in result.strategies
        ]

        summary = ReportSummary(
            has_recommendations=(
                len(reports) > 0
            ),
            total_strategies=len(
                reports,
            ),
            total_recommendations=sum(
                1 + len(report.alternatives)
                for report in reports
            ),
            validated_recommendations=sum(
                1
                for report in reports
                if report.validation.status
                == "validated"
            ),
            estimated_improvement_percent=max(
                (
                    report.validation.improvement_percent
                    for report in reports
                ),
                default=0.0,
            ),
            highest_strategy_score=max(
                (
                    report.overall_score
                    for report in reports
                ),
                default=0.0,
            ),
        )

        return OptimizationReport(
            summary=summary,
            strategies=reports,
        )