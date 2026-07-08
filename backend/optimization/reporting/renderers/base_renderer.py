from __future__ import annotations

from abc import ABC, abstractmethod

from backend.optimization.reporting.models.optimization_report import (
    OptimizationReport,
)


class ReportRenderer(
    ABC,
):
    """
    Renders an optimization report into an output format.
    """

    @property
    @abstractmethod
    def name(
        self,
    ) -> str:
        """
        Unique renderer name.
        """

    @abstractmethod
    def render(
        self,
        report: OptimizationReport,
    ) -> str:
        """
        Render the report.
        """