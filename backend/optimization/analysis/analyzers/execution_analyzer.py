from __future__ import annotations

from backend.optimization.analysis.analyzers.base_analyzer import Analyzer
from backend.optimization.analysis.context import AnalysisContext
from backend.optimization.analysis.models.finding_collection import FindingCollection
from backend.optimization.analysis.registry.rule_registry import RuleRegistry
from backend.optimization.analysis.rules.base_rule import AnalysisRule


class ExecutionAnalyzer(Analyzer):
    """
    Coordinates execution analysis rules.

    The analyzer owns orchestration only.
    Individual optimization phenomena are detected by independent rules.
    """

    def __init__(
        self,
        registry: RuleRegistry,
    ) -> None:
        self._registry = registry

    @property
    def name(self) -> str:
        return "execution"

    def analyze(
        self,
        context: AnalysisContext,
    ) -> FindingCollection:

        findings = FindingCollection()

        for rule in self._registry:

            if not isinstance(rule, AnalysisRule):
                continue

            findings.extend(
                rule.analyze(context)
            )

        return findings