from __future__ import annotations

from collections.abc import Iterator

from backend.optimization.analysis.rules.base_rule import AnalysisRule


class RuleRegistry:
    """
    Registry of analysis rules.

    The registry owns rule registration but not execution.
    """

    def __init__(self) -> None:
        self._rules: list[AnalysisRule] = []

    def register(
        self,
        rule: AnalysisRule,
    ) -> None:
        self._rules.append(rule)

    def __iter__(self) -> Iterator[AnalysisRule]:
        return iter(self._rules)

    def __len__(self) -> int:
        return len(self._rules)