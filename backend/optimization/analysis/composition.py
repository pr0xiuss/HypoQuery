from __future__ import annotations

from backend.optimization.analysis.analyzers.configuration_analyzer import (
    ConfigurationAnalyzer,
)
from backend.optimization.analysis.analyzers.health_analyzer import (
    HealthAnalyzer,
)
from backend.optimization.analysis.analyzers.workload_analyzer import (
    WorkloadAnalyzer,
)
from backend.optimization.analysis.bootstrap import (
    build_execution_analyzer,
)
from backend.optimization.analysis.engine import AnalysisEngine
from backend.optimization.analysis.registry.analyzer_registry import (
    AnalyzerRegistry,
)


def build_analysis_engine() -> AnalysisEngine:
    """
    Composition root for the Analysis bounded context.

    Assembles all analysis domains behind a single AnalysisEngine.
    """

    registry = AnalyzerRegistry()

    registry.register(
        build_execution_analyzer()
    )

    registry.register(
        HealthAnalyzer()
    )

    registry.register(
        ConfigurationAnalyzer()
    )

    registry.register(
        WorkloadAnalyzer()
    )

    return AnalysisEngine(
        registry=registry,
    )