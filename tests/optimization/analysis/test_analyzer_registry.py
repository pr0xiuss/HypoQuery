from backend.optimization.analysis.analyzers.base_analyzer import (
    Analyzer,
)
from backend.optimization.analysis.context import AnalysisContext
from backend.optimization.analysis.models.finding_collection import (
    FindingCollection,
)
from backend.optimization.analysis.registry.analyzer_registry import (
    AnalyzerRegistry,
)


class DummyAnalyzer(Analyzer):

    @property
    def name(self) -> str:
        return "dummy"

    def analyze(
        self,
        context: AnalysisContext,
    ) -> FindingCollection:
        return FindingCollection()


def test_register_analyzer():

    registry = AnalyzerRegistry()

    analyzer = DummyAnalyzer()

    registry.register(analyzer)

    analyzers = list(registry)

    assert len(analyzers) == 1
    assert analyzers[0] is analyzer