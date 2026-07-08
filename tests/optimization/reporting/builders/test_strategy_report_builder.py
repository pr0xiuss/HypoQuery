from backend.optimization.reporting.builders.recommendation_report_builder import (
    RecommendationReportBuilder,
)
from backend.optimization.reporting.builders.strategy_report_builder import (
    StrategyReportBuilder,
)
from backend.optimization.reporting.builders.validation_report_builder import (
    ValidationReportBuilder,
)
from backend.optimization.ranking.grouping.models.strategy import (
    Strategy,
)
from backend.optimization.ranking.grouping.models.strategy_type import (
    StrategyType,
)
from backend.optimization.ranking.models.ranking import (
    Ranking,
)
from tests.optimization.ranking.models.test_ranking_result import (
    create_ranking,
)


def test_build():

    ranking = create_ranking(score=85.0)

    strategy = Strategy(
        strategy_type=StrategyType.INDEXING,
        representative=ranking,
        alternatives=[],
    )

    builder = StrategyReportBuilder(
        RecommendationReportBuilder(),
        ValidationReportBuilder(),
    )

    report = builder.build(
        strategy,
    )

    assert (
        report.strategy
        == StrategyType.INDEXING
    )

    assert (
        report.representative.title
        == ranking.recommendation.title
    )

    assert report.overall_score == strategy.overall_score