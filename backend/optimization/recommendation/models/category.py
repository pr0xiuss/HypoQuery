from enum import StrEnum


class RecommendationCategory(StrEnum):
    """
    High-level category describing the type of recommendation.
    """

    INDEX = "index"

    CONFIGURATION = "configuration"

    QUERY_REWRITE = "query_rewrite"

    STATISTICS = "statistics"

    PARTITIONING = "partitioning"

    PARALLELISM = "parallelism"

    MAINTENANCE = "maintenance"

    GENERAL = "general"