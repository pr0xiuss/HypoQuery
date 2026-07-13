from __future__ import annotations

from dataclasses import dataclass

from backend.optimization.recommendation.models.recommendation_key import (
    RecommendationKey,
)


@dataclass(
    frozen=True,
    slots=True,
)
class RecommendationReference:
    """
    Immutable reference to a recommendation produced by
    the Optimization bounded context.

    Operations intentionally references the recommendation's
    business identity rather than its persistence identity.
    """

    key: RecommendationKey

    recommendation_code: str

    recommendation_version: int = 1