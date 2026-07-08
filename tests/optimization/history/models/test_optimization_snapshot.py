from backend.optimization.history.models.optimization_snapshot import (
    OptimizationSnapshot,
)
from backend.optimization.reporting.models.optimization_report import (
    OptimizationReport,
)
from backend.optimization.reporting.models.report_summary import (
    ReportSummary,
)


def test_optimization_snapshot():

    report = OptimizationReport(
        summary=ReportSummary(),
    )

    snapshot = OptimizationSnapshot(
        report=report,
    )

    assert snapshot.report == report