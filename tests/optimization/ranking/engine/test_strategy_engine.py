

from backend.optimization.ranking.grouping.engine import (
    StrategyEngine,
)
from backend.optimization.ranking.grouping.context import (
    StrategyContext,
)
from backend.optimization.ranking.grouping.groupers.default_grouper import (
    DefaultStrategyGrouper,
)
from backend.optimization.ranking.grouping.models.strategy_type import (
    StrategyType,
)
from backend.optimization.ranking.grouping.registry import (
    StrategyRegistry,
)
from backend.optimization.ranking.models.ranking import (
    Ranking,
)
from backend.optimization.ranking.models.ranking_dimension import (
    RankingDimension,
)
from backend.optimization.ranking.models.ranking_result import (
    RankingResult,
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
        code=f"IDX_{score}",
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


def test_group():

    registry = StrategyRegistry()

    registry.register(
        DefaultStrategyGrouper(),
    )

    engine = StrategyEngine(
        registry,
    )

    rankings = RankingResult()

    rankings.add(
        create_ranking(90),
    )

    rankings.add(
        create_ranking(80),
    )

    result = engine.group(
        StrategyContext(
            ranking_result=rankings,
        )
    )

    assert len(result.strategies) == 1

    assert (
        result.strategies[0].strategy_type
        == StrategyType.INDEXING
    )

    assert (
        len(
            result.strategies[0].alternatives
        )
        == 1
    )