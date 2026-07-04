from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RecommendationKey:
    """
    Stable identifier describing what this recommendation targets.

    RecommendationKey is used for deduplication, validation,
    ranking and reporting.
    """

    category: str

    target: str

    action: str