from __future__ import annotations

from enum import StrEnum


class ContextPriority(StrEnum):
    """
    Relative importance of a context section.

    Priorities determine how the assembled optimization
    context is presented to downstream consumers.
    """

    PRIMARY = "primary"

    SECONDARY = "secondary"

    SUPPORTING = "supporting"