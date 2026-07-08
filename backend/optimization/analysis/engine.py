from __future__ import annotations

from backend.optimization.analysis.context import AnalysisContext
from backend.optimization.analysis.models.analysis_result import AnalysisResult
from backend.optimization.analysis.registry.analyzer_registry import (
    AnalyzerRegistry,
)


class AnalysisEngine:
    """
    Entry point of the Analysis bounded context.

    Coordinates all analysis domains and publishes
    one AnalysisResult.
    """

    def __init__(self, registry: AnalyzerRegistry,) -> None:
        
        self._registry = registry

    def analyze(self, context: AnalysisContext,) -> AnalysisResult:

        result = AnalysisResult()

        for analyzer in self._registry:
            result.findings.extend(
                analyzer.analyze(context)
            )

        return result