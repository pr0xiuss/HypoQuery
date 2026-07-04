from enum import IntEnum


class RecommendationPriority(IntEnum):
    """
    Execution priority for recommendations.

    Higher values indicate more important recommendations.
    """

    LOW = 1

    MEDIUM = 2

    HIGH = 3

    CRITICAL = 4