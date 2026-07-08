from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RecommendationLocation:
    """
    Identifies the database object affected by a recommendation.

    Unlike Analysis, this represents where the recommendation
    should be applied rather than where an observation occurred.
    """

    relation: str | None = None

    schema: str | None = None

    index: str | None = None

    column: str | None = None