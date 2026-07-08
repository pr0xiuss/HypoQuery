from __future__ import annotations

from backend.optimization.analysis.analyzers.base_analyzer import Analyzer
from backend.optimization.analysis.context import AnalysisContext
from backend.optimization.analysis.models.finding_collection import (
    FindingCollection,
)


class WorkloadAnalyzer(Analyzer):
    """
    Coordinates workload analysis rules.

    Workload analysis is introduced in later modules.
    """

    @property
    def name(self) -> str:
        return "workload"

    def analyze(
        self,
        context: AnalysisContext,
    ) -> FindingCollection:

        return FindingCollection()