from __future__ import annotations

from enum import Enum


class StrategyType(str, Enum):
    """
    High-level optimization strategy.
    """

    INDEXING = "indexing"

    QUERY_REWRITE = "query_rewrite"

    MEMORY = "memory"

    PARTITIONING = "partitioning"

    CONFIGURATION = "configuration"

    OTHER = "other"