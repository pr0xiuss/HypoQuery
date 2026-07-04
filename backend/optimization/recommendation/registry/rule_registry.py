from __future__ import annotations

from collections.abc import Iterator

from backend.optimization.recommendation.rules.base_rule import (
    RecommendationRule,
)


class RecommendationRuleRegistry:
    """
    Stores every registered recommendation rule.

    Registration occurs only from the composition root.
    """

    def __init__(self) -> None:

        self._rules: list[RecommendationRule] = []

    def register(
        self,
        rule: RecommendationRule,
    ) -> None:

        self._rules.append(rule)

    def __iter__(self) -> Iterator[RecommendationRule]:

        return iter(self._rules)

    def __len__(self) -> int:

        return len(self._rules)