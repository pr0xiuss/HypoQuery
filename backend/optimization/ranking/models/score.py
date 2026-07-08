from __future__ import annotations
from backend.optimization.ranking.models.ranking_dimension import RankingDimension
from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Score:
    """
    Represents the score produced by a single ranking dimension.
    """
    dimension: RankingDimension

    score: float

    reason: str