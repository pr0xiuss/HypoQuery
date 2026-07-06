from backend.optimization.ranking.grouping.models.strategy import (
    Strategy,
)
from backend.optimization.ranking.grouping.models.strategy_result import (
    StrategyResult,
)
from backend.optimization.ranking.grouping.models.strategy_type import (
    StrategyType,
)
from backend.optimization.ranking.models.ranking import (
    Ranking,
)
from backend.optimization.ranking.models.ranking_dimension import (
    RankingDimension,
)
from backend.optimization.ranking.models.score import (
    Score,
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


def create_strategy(
    strategy_type: StrategyType,
    score: float,
) -> Strategy:

    recommendation = Recommendation(
        category=RecommendationCategory.INDEX,
        code=f"CREATE_INDEX_{score}",
        key=RecommendationKey(
            category="index",
            target=f"users_{score}",
            action="create",
        ),
        title="Create Index",
        description="",
        priority=RecommendationPriority.HIGH,
    )

    ranking = Ranking(
        recommendation=recommendation,
        validation=None,
        scores={
            RankingDimension.IMPACT: Score(
                dimension=RankingDimension.IMPACT,
                score=score,
                reason="",
            ),
        },
        total_score=score,
    )

    return Strategy(
        strategy_type=strategy_type,
        representative=ranking,
    )


def test_add_and_get():

    result = StrategyResult()

    strategy = create_strategy(
        StrategyType.INDEXING,
        90,
    )

    result.add(
        strategy,
    )

    assert (
        result.get(
            StrategyType.INDEXING,
        )
        == strategy
    )


def test_sort():

    result = StrategyResult()

    result.add(
        create_strategy(
            StrategyType.MEMORY,
            50,
        )
    )

    result.add(
        create_strategy(
            StrategyType.INDEXING,
            95,
        )
    )

    result.sort()

    assert (
        result.strategies[0].overall_score
        == 95
    )

    assert (
        result.strategies[1].overall_score
        == 50
    )