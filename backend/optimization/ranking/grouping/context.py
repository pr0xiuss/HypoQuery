from __future__ import annotations

from dataclasses import dataclass

from backend.optimization.ranking.models.ranking_result import (
    RankingResult,
)


@dataclass(slots=True, frozen=True)
class StrategyContext:
    """
    Input for the strategy engine.
    """

    ranking_result: RankingResult