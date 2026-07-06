from __future__ import annotations

from abc import ABC, abstractmethod

from backend.optimization.ranking.context import (
    RankingContext,
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


class RankingScorer(ABC):
    """
    Base contract implemented by every ranking scorer.
    """

    @property
    @abstractmethod
    def name(
        self,
    ) -> str:
        ...

    @abstractmethod
    def score(
        self,
        context: RankingContext,
        recommendation: Recommendation,
        validation: Validation | None,
    ) -> Score:
        ...