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


def test_ranking():

    recommendation = Recommendation(
        category=RecommendationCategory.INDEX,
        code="CREATE_INDEX",
        key=RecommendationKey(
            category="index",
            target="users",
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
                score=95,
                reason="Improved.",
            ),
        },
        total_score=95,
    )

    assert ranking.recommendation == recommendation

    assert ranking.total_score == 95

    assert (
        RankingDimension.IMPACT
        in ranking.scores
    )