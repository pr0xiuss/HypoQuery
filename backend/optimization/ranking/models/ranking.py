from __future__ import annotations

from dataclasses import dataclass

from backend.optimization.ranking.models.ranking_dimension import (
    RankingDimension,
)
from backend.optimization.ranking.models.score import (
    Score,
)
from backend.optimization.recommendation.models.recommendation import (
    Recommendation,
)
from backend.optimization.validation.models.validation import (
    Validation,
)


@dataclass(slots=True, frozen=True)
class Ranking:
    """
    Final ranking produced for a recommendation.
    """

    recommendation: Recommendation

    validation: Validation | None

    scores: dict[
        RankingDimension,
        Score,
    ]

    total_score: float