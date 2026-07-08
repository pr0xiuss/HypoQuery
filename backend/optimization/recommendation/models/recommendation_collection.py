from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterator

from backend.optimization.recommendation.models.recommendation import (
    Recommendation,
)


@dataclass(slots=True)
class RecommendationCollection:
    """
    Represents all recommendations generated during a single
    recommendation execution.

    RecommendationResult is the aggregate root exposed outside
    the Recommendation bounded context.
    """

    recommendations: list[Recommendation] = field(
        default_factory=list,
    )

    def add(
        self,
        recommendation: Recommendation,
    ) -> None:

        self.recommendations.append(
            recommendation,
        )

    def extend(
        self,
        recommendations: "RecommendationCollection",
    ) -> None:

        self.recommendations.extend(
            recommendations,
        )

    def __iter__(self) -> Iterator[Recommendation]:

        return iter(
            self.recommendations,
        )

    def __len__(self) -> int:

        return len(
            self.recommendations,
        )

    def is_empty(self) -> bool:

        return len(
            self.recommendations,
        ) == 0