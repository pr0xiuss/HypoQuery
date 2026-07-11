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

    summary = ReportSummary()

    snapshot = OptimizationSnapshot(
        summary=summary,
    )

    assert snapshot.summary == summary
    assert snapshot.findings == ()
    assert snapshot.recommendations == ()
    assert snapshot.validations == ()
    assert snapshot.strategies == ()