from __future__ import annotations

from backend.optimization.analysis.analyzers.base_analyzer import Analyzer
from backend.optimization.analysis.context import AnalysisContext
from backend.optimization.analysis.models.finding_collection import (
    FindingCollection,
)


class ConfigurationAnalyzer(Analyzer):
    """
    Coordinates configuration analysis rules.

    Configuration analysis is introduced in later modules.
    """

    @property
    def name(self) -> str:
        return "configuration"

    def analyze(
        self,
        context: AnalysisContext,
    ) -> FindingCollection:

        return FindingCollection()