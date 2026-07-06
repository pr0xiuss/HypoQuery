from __future__ import annotations

from enum import Enum


class ValidationType(str, Enum):
    """
    Describes the strategy used to validate a recommendation.
    """

    HYPOTHETICAL_INDEX = "hypothetical_index"

    CONFIGURATION = "configuration"

    STATISTICS = "statistics"

    MANUAL = "manual"