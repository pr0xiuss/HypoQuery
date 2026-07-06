from backend.optimization.ranking.registry.scorer_registry import (
    ScorerRegistry,
)
from backend.optimization.ranking.scorers.base_scorer import (
    RankingScorer,
)
from backend.optimization.ranking.context import (
    RankingContext,
)
from backend.optimization.ranking.models.ranking_dimension import (
    RankingDimension,
)
from backend.optimization.ranking.models.score import (
    Score,
)


class DummyScorer(
    RankingScorer,
):

    @property
    def name(
        self,
    ) -> str:

        return "dummy"

    def score(
        self,
        context: RankingContext,
        recommendation,
        validation,
    ) -> Score:

        return Score(
            dimension=RankingDimension.IMPACT,
            score=100,
            reason="",
        )


def test_register():

    registry = ScorerRegistry()

    registry.register(
        DummyScorer(),
    )

    assert len(registry) == 1

    assert list(registry)[0].name == "dummy"