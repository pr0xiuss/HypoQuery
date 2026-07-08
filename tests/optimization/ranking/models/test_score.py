from backend.optimization.ranking.models.ranking_dimension import (
    RankingDimension,
)
from backend.optimization.ranking.models.score import (
    Score,
)


def test_score():

    score = Score(
        dimension=RankingDimension.IMPACT,
        score=92.5,
        reason="Validated improvement.",
    )

    assert score.dimension == RankingDimension.IMPACT

    assert score.score == 92.5

    assert score.reason == "Validated improvement."