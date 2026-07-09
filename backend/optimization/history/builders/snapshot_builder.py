from __future__ import annotations

from backend.execution.contracts.execution import (
    PipelineExecution,
)
from backend.optimization.history.models.optimization_snapshot import (
    OptimizationSnapshot,
)
from backend.optimization.reporting.models.report_summary import (
    ReportSummary,
)


class SnapshotBuilder:
    """
    Builds optimization snapshots from pipeline execution state.
    """

    def build(
        self,
        execution: PipelineExecution,
    ) -> OptimizationSnapshot:

        report = execution.state.report

        summary = (
            report.summary
            if report is not None
            else ReportSummary()
        )

        return OptimizationSnapshot(
            summary=summary,
            findings=(
                tuple(
                    execution.state.analysis_result.findings.findings
                )
                if execution.state.analysis_result is not None
                else ()
            ),
            recommendations=(
                tuple(
                    execution.state.recommendation_result
                    .recommendations.recommendations
                )
                if execution.state.recommendation_result is not None
                else ()
            ),
            validations=(
                tuple(
                    execution.state.validation_result
                    .validations.validations
                )
                if execution.state.validation_result is not None
                else ()
            ),
            strategies=(
                tuple(
                    execution.state.strategy_result.strategies
                )
                if execution.state.strategy_result is not None
                else ()
            ),
        )