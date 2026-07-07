from backend.optimization.reporting.builders.optimization_report_builder import (
    OptimizationReportBuilder,
)
from backend.optimization.reporting.builders.recommendation_report_builder import (
    RecommendationReportBuilder,
)
from backend.optimization.reporting.builders.strategy_report_builder import (
    StrategyReportBuilder,
)
from backend.optimization.reporting.builders.validation_report_builder import (
    ValidationReportBuilder,
)
from backend.optimization.ranking.grouping.models.strategy_result import (
    StrategyResult,
)
from tests.optimization.ranking.models.test_strategy_result import (
    create_strategy,
)
from backend.optimization.ranking.grouping.models.strategy_type import (
    StrategyType,
)

def test_build():

    result = StrategyResult()

    result.add(
        create_strategy(strategy_type=StrategyType.INDEXING, score=85.0),
    )

    builder = OptimizationReportBuilder(
        StrategyReportBuilder(
            RecommendationReportBuilder(),
            ValidationReportBuilder(),
        )
    )

    report = builder.build(
        result,
    )

    assert report.summary.has_recommendations

    assert report.summary.total_strategies == 1

    assert len(report.strategies) == 1