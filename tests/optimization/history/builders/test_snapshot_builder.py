from backend.optimization.history.builders.snapshot_builder import (
    SnapshotBuilder,
)
from backend.optimization.reporting.models.optimization_report import (
    OptimizationReport,
)
from backend.optimization.reporting.models.report_summary import (
    ReportSummary,
)


def test_build():

    report = OptimizationReport(
        summary=ReportSummary(),
    )

    builder = SnapshotBuilder()

    snapshot = builder.build(
        report,
    )

    assert snapshot.report == report