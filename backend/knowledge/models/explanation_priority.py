from __future__ import annotations

from enum import StrEnum


class ExplanationPriority(StrEnum):
    """
    Relative importance of an explanation section.

    Priorities determine the ordering of explanation
    content presented to downstream consumers.
    """

    PRIMARY = "primary"

    SECONDARY = "secondary"

    SUPPORTING = "supporting"