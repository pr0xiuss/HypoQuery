from __future__ import annotations

from collections.abc import Iterator

from backend.optimization.analysis.analyzers.base_analyzer import Analyzer


class AnalyzerRegistry:
    """
    Registry of analysis domain analyzers.

    The registry owns analyzer registration but not orchestration.
    """

    def __init__(self) -> None:
        self._analyzers: list[Analyzer] = []

    def register(
        self,
        analyzer: Analyzer,
    ) -> None:
        self._analyzers.append(analyzer)

    def __iter__(self) -> Iterator[Analyzer]:
        return iter(self._analyzers)

    def __len__(self) -> int:
        return len(self._analyzers)