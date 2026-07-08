from __future__ import annotations

from backend.optimization.ranking.grouping.base_grouper import (
    StrategyGrouper,
)
from backend.optimization.ranking.grouping.models.strategy_type import (
    StrategyType,
)
from backend.optimization.ranking.models.ranking import (
    Ranking,
)
from backend.optimization.recommendation.models.category import (
    RecommendationCategory,
)


class DefaultStrategyGrouper(
    StrategyGrouper,
):
    """
    Default deterministic strategy classifier.
    """

    @property
    def name(
        self,
    ) -> str:

        return "default"

    def classify(
        self,
        ranking: Ranking,
    ) -> StrategyType | None:

        category = (
            ranking.recommendation.category
        )

        if category == RecommendationCategory.INDEX:

            return StrategyType.INDEXING

        if category == RecommendationCategory.QUERY_REWRITE:

            return StrategyType.QUERY_REWRITE

        if category == RecommendationCategory.PARTITIONING:

            return StrategyType.PARTITIONING

        if category == RecommendationCategory.CONFIGURATION:

            return StrategyType.CONFIGURATION

        if category in (
            RecommendationCategory.STATISTICS,
            RecommendationCategory.PARALLELISM,
            RecommendationCategory.MAINTENANCE,
            RecommendationCategory.GENERAL,
        ):

            return StrategyType.OTHER

        return StrategyType.OTHER