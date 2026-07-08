from __future__ import annotations

from enum import Enum


class RankingDimension(str, Enum):
    """
    Dimensions contributing to the final recommendation ranking.
    """

    IMPACT = "impact"

    CONFIDENCE = "confidence"

    VALIDATION = "validation"

    RISK = "risk"

    URGENCY = "urgency"