from backend.optimization.ranking.models.ranking_dimension import (
    RankingDimension,
)
from backend.optimization.ranking.scorers.risk_scorer import (
    RiskScorer,
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


def create_recommendation(
    category: RecommendationCategory,
) -> Recommendation:

    return Recommendation(
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


def test_index_recommendation_low_risk():

    scorer = RiskScorer()

    recommendation = create_recommendation(
        RecommendationCategory.INDEX,
    )

    score = scorer.score(
        context=None,
        recommendation=recommendation,
        validation=None,
    )

    assert (
        score.dimension
        == RankingDimension.RISK
    )

    assert score.score == 90

    assert (
        "low risk"
        in score.reason.lower()
    )


def test_non_index_recommendation_default_risk():

    scorer = RiskScorer()

    recommendation = create_recommendation(
        RecommendationCategory.QUERY_REWRITE,
    )

    score = scorer.score(
        context=None,
        recommendation=recommendation,
        validation=None,
    )

    assert (
        score.dimension
        == RankingDimension.RISK
    )

    assert score.score == 50

    assert (
        "moderate"
        in score.reason.lower()
    )