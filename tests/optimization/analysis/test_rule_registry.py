from backend.optimization.analysis.registry.rule_registry import (
    RuleRegistry,
)
from backend.optimization.analysis.rules.base_rule import (
    AnalysisRule,
)
from backend.optimization.analysis.context import AnalysisContext
from backend.optimization.analysis.models.finding_collection import (
    FindingCollection,
)


class DummyRule(AnalysisRule):

    @property
    def name(self) -> str:
        return "dummy"

    def analyze(
        self,
        context: AnalysisContext,
    ) -> FindingCollection:
        return FindingCollection()


def test_register_rule():

    registry = RuleRegistry()

    rule = DummyRule()

    registry.register(rule)

    rules = list(registry)

    assert len(rules) == 1
    assert rules[0] is rule