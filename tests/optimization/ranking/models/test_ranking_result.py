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


def test_sort():

    result = RankingResult()

    result.add(
        create_ranking(50),
    )

    result.add(
        create_ranking(90),
    )

    result.add(
        create_ranking(75),
    )

    result.sort()

    assert (
        result.rankings[0].total_score
        == 90
    )

    assert (
        result.rankings[1].total_score
        == 75
    )

    assert (
        result.rankings[2].total_score
        == 50
    )