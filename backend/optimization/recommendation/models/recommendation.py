from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4
from backend.optimization.recommendation.models.recommendation_key import RecommendationKey
from backend.optimization.recommendation.models.category import RecommendationCategory
from backend.optimization.recommendation.models.location import RecommendationLocation
from backend.optimization.recommendation.models.metadata import RecommendationMetadata
from backend.optimization.recommendation.models.priority import RecommendationPriority


@dataclass(slots=True)
class Recommendation:
    """
    Represents a deterministic optimization recommendation.

    A Recommendation answers the question:

        "What should be done?"

    It is derived from one or more Findings and never directly
    inspects execution plans.
    """

    category: RecommendationCategory

    code: str

    key: RecommendationKey

    title: str

    description: str

    priority: RecommendationPriority

    confidence: float = 1.0

    location: RecommendationLocation = field(
        default_factory=RecommendationLocation,
    )

    metadata: RecommendationMetadata = field(
        default_factory=RecommendationMetadata,
    )

    id: UUID = field(default_factory=uuid4)

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )