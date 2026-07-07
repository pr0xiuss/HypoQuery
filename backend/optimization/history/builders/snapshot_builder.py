from __future__ import annotations

from backend.optimization.history.models.optimization_snapshot import (
    OptimizationSnapshot,
)
from backend.optimization.reporting.models.optimization_report import (
    OptimizationReport,
)


class SnapshotBuilder:
    """
    Builds optimization snapshots from optimization reports.
    """

    def build(
        self,
        report: OptimizationReport,
    ) -> OptimizationSnapshot:

        return OptimizationSnapshot(
            report=report,
        )