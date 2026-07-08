from __future__ import annotations

from backend.optimization.reporting.builders.optimization_report_builder import (
    OptimizationReportBuilder,
)
from backend.optimization.reporting.context import (
    ReportingContext,
)
from backend.optimization.reporting.models.optimization_report import (
    OptimizationReport,
)


class ReportingEngine:
    """
    Coordinates construction of the published optimization report.
    """

    def __init__(
        self,
        report_builder: OptimizationReportBuilder,
    ) -> None:

        self._report_builder = report_builder

    def generate(
        self,
        context: ReportingContext,
    ) -> OptimizationReport:

        return self._report_builder.build(
            context.strategy_result,
        )