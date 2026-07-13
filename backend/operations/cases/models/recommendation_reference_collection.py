from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field

from backend.operations.models.references import (
    RecommendationReference,
)


@dataclass(
    slots=True,
)
class RecommendationReferenceCollection:
    """
    Collection of recommendation references
    associated with an Optimization Case.
    """

    recommendations: list[RecommendationReference] = field(
        default_factory=list,
    )

    def add(
        self,
        recommendation: RecommendationReference,
    ) -> None:
        if recommendation in self.recommendations:
            return

        self.recommendations.append(
            recommendation,
        )

    def __len__(self) -> int:
        return len(
            self.recommendations,
        )

    def __iter__(self) -> Iterator[RecommendationReference]:
        return iter(
            self.recommendations,
        )
    
    def contains(
        self,
        recommendation: RecommendationReference,
    ) -> bool:
        return recommendation in self.recommendations
    
    def __getitem__(
        self,
        index: int,
    ) -> RecommendationReference:
        return self.recommendations[index]