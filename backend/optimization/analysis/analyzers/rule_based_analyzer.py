from __future__ import annotations

from abc import abstractmethod
from collections.abc import Iterable

from backend.optimization.analysis.analyzers.base_analyzer import Analyzer
from backend.optimization.analysis.context import AnalysisContext
from backend.optimization.analysis.models.finding_collection import (
    FindingCollection,
)
from backend.optimization.analysis.rules.base_rule import AnalysisRule


class RuleBasedAnalyzer(Analyzer):
    """
    Base implementation for analyzers that execute a collection
    of independent Analysis Rules.

    Implements the Template Method pattern by providing the
    common rule execution workflow while allowing subclasses
    to define their identity.
    """

    def __init__(self, rules: Iterable[AnalysisRule]) -> None:
        self._rules = tuple(rules)

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    def analyze(self, context: AnalysisContext) -> FindingCollection:
        findings = FindingCollection()

        for rule in self._rules:
            findings.extend(rule.analyze(context))

        return findings