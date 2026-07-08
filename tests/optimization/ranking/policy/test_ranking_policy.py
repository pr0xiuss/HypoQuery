from backend.optimization.ranking.models.ranking_dimension import (
    RankingDimension,
)
from backend.optimization.ranking.models.score import (
    Score,
)
from backend.optimization.ranking.policy import (
    RankingPolicy,
)


def test_calculate():

    policy = RankingPolicy()

    scores = [
        Score(
            dimension=RankingDimension.IMPACT,
            score=100,
            reason="",
        ),
        Score(
            dimension=RankingDimension.VALIDATION,
            score=100,
            reason="",
        ),
        Score(
            dimension=RankingDimension.CONFIDENCE,
            score=100,
            reason="",
        ),
        Score(
            dimension=RankingDimension.RISK,
            score=100,
            reason="",
        ),
    ]

    assert (
        policy.calculate(scores)
        == 100
    )