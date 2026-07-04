from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from backend.optimization.recommendation.models.recommendation_collection import (
    RecommendationCollection,
)


@dataclass(slots=True)
class RecommendationResult:
    """
    Published contract of the Recommendation bounded context.

    Represents the complete set of deterministic recommendations
    produced during one recommendation execution.
    """

    recommendations: RecommendationCollection = field(
        default_factory=RecommendationCollection,
    )

    started_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )

    completed_at: datetime | None = None

    metadata: dict[str, object] = field(
        default_factory=dict,
    )

    @property
    def total_recommendations(self) -> int:

        return len(
            self.recommendations,
        )