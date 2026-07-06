from backend.optimization.ranking.grouping.base_grouper import (
    StrategyGrouper,
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


class DummyGrouper(
    StrategyGrouper,
):

    @property
    def name(
        self,
    ) -> str:

        return "dummy"

    def classify(
        self,
        ranking: Ranking,
    ) -> StrategyType | None:

        return StrategyType.OTHER


def test_find_strategy_type():

    registry = StrategyRegistry()

    registry.register(
        DummyGrouper(),
    )

    assert (
        registry.find_strategy_type(
            None,
        )
        == StrategyType.OTHER
    )

    assert len(registry) == 1