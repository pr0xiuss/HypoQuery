from __future__ import annotations

from dataclasses import dataclass

from backend.optimization.reporting.models.optimization_report import (
    OptimizationReport,
)


@dataclass(frozen=True, slots=True)
class OptimizationSnapshot:
    """
    Immutable snapshot of the optimization output
    produced during one execution.
    """

    report: OptimizationReport