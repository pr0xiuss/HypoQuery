from backend.optimization.recommendation.context import (
    RecommendationContext,
)
from backend.optimization.recommendation.models.recommendation_collection import (
    RecommendationCollection,
)
from backend.optimization.recommendation.registry.rule_registry import (
    RecommendationRuleRegistry,
)
from backend.optimization.recommendation.rules.base_rule import (
    RecommendationRule,
)


class DummyRule(RecommendationRule):

    @property
    def name(self) -> str:
        return "dummy"

    def recommend(
        self,
        context: RecommendationContext,
    ) -> RecommendationCollection:

        return RecommendationCollection()


def test_register():

    registry = RecommendationRuleRegistry()

    rule = DummyRule()

    registry.register(
        rule,
    )

    assert len(registry) == 1


def test_iterates_registered_rules():

    registry = RecommendationRuleRegistry()

    registry.register(
        DummyRule(),
    )

    rules = list(
        registry,
    )

    assert len(rules) == 1

    assert rules[0].name == "dummy"