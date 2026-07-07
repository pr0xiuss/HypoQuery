from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from backend.optimization.reporting.models.report_summary import (
    ReportSummary,
)
from backend.optimization.reporting.models.strategy_report import (
    StrategyReport,
)


@dataclass(slots=True)
class OptimizationReport:
    """
    Published contract of the Reporting bounded context.
    """

    summary: ReportSummary

    strategies: list[
        StrategyReport
    ] = field(
        default_factory=list,
    )

    generated_at: datetime = field(
        default_factory=lambda: datetime.now(
            UTC,
        )
    )