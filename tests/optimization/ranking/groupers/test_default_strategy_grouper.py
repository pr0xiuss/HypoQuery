from backend.optimization.ranking.grouping.groupers.default_grouper import (
    DefaultStrategyGrouper,
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
from backend.optimization.recommendation.models.priority import (
    RecommendationPriority,
)
from backend.optimization.recommendation.models.recommendation import (
    Recommendation,
)
from backend.optimization.recommendation.models.recommendation_key import (
    RecommendationKey,
)


def create_ranking(
    category: RecommendationCategory,
) -> Ranking:

    recommendation = Recommendation(
        category=category,
        code="TEST",
        key=RecommendationKey(
            category=category.value,
            target="users",
            action="create",
        ),
        title="Test",
        description="",
        priority=RecommendationPriority.HIGH,
    )

    return Ranking(
        recommendation=recommendation,
        validation=None,
        scores={},
        total_score=0,
    )


def test_index_strategy():

    grouper = DefaultStrategyGrouper()

    ranking = create_ranking(
        RecommendationCategory.INDEX,
    )

    assert (
        grouper.classify(
            ranking,
        )
        == StrategyType.INDEXING
    )

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

def test_configuration_strategy():

    grouper = DefaultStrategyGrouper()

    ranking = create_ranking(
        RecommendationCategory.CONFIGURATION,
    )

    assert (
        grouper.classify(
            ranking,
        )
        == StrategyType.CONFIGURATION
    )