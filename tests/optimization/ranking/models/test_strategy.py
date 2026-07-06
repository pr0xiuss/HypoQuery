from backend.optimization.ranking.grouping.models.strategy import (
    Strategy,
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


def create_ranking(
    score: float,
) -> Ranking:

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

    return Ranking(
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


def test_strategy():

    representative = create_ranking(
        95,
    )

    alternative = create_ranking(
        82,
    )

    strategy = Strategy(
        strategy_type=StrategyType.INDEXING,
        representative=representative,
    )

    strategy.add_alternative(
        alternative,
    )

    assert (
        strategy.strategy_type
        == StrategyType.INDEXING
    )

    assert (
        strategy.representative
        == representative
    )

    assert (
        len(strategy.alternatives)
        == 1
    )

    assert (
        strategy.overall_score
        == 95
    )