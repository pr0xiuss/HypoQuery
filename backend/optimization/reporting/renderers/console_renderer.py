from __future__ import annotations

from backend.optimization.reporting.formatters.report_formatter import ReportFormatter
from backend.optimization.reporting.models.optimization_report import OptimizationReport
from backend.optimization.reporting.renderers.base_renderer import ReportRenderer


class ConsoleRenderer(ReportRenderer):
    """
    Renders an optimization report for terminal output.
    """

    def __init__(self, formatter: ReportFormatter) -> None:

        self._formatter = formatter

    @property
    def name(self) -> str:

        return "console"

    def render(self, report: OptimizationReport) -> str:

        summary = report.summary

        lines: list[str] = [
            "Optimization Report",
            "=" * 60,
            "",
            "Summary",
            "-" * 60,
            f"Strategies            : {summary.total_strategies}",
            f"Recommendations       : {summary.total_recommendations}",
            f"Validated             : {summary.validated_recommendations}",
            (
                "Estimated Improvement : "
                f"{self._formatter.percentage(summary.estimated_improvement_percent)}"
            ),
            (
                "Highest Score         : "
                f"{self._formatter.score(summary.highest_strategy_score)}"
            ),
            "",
        ]

        for strategy in report.strategies:

            lines.append(
                f"[{self._formatter.strategy(strategy.strategy)}]"
            )

            lines.append(
                f"Score          : "
                f"{self._formatter.score(strategy.overall_score)}"
            )

            lines.append(
                f"Recommendation : "
                f"{strategy.representative.title}"
            )

            lines.append(
                f"Priority       : "
                f"{self._formatter.priority(strategy.representative.priority)}"
            )

            lines.append(
                f"Category       : "
                f"{self._formatter.category(strategy.representative.category)}"
            )

            lines.append(
                f"Validated      : "
                f"{self._formatter.validation_status(strategy.validation.status)}"
            )

            lines.append(
                f"Improvement    : "
                f"{self._formatter.percentage(strategy.validation.improvement_percent)}"
            )

            if strategy.alternatives:

                lines.append(
                    "Alternatives:"
                )

                for alternative in strategy.alternatives:

                    lines.append(
                        f"  - {alternative.title}"
                    )

            lines.append("")

        return "\n".join(lines)