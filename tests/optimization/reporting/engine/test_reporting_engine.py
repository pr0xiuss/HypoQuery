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
from backend.optimization.reporting.context import (
    ReportingContext,
)
from backend.optimization.reporting.engine import (
    ReportingEngine,
)
from backend.optimization.ranking.grouping.models.strategy_result import (
    StrategyResult,
)


def test_generate():

    engine = ReportingEngine(
        OptimizationReportBuilder(
            StrategyReportBuilder(
                RecommendationReportBuilder(),
                ValidationReportBuilder(),
            )
        )
    )

    report = engine.generate(
        ReportingContext(
            strategy_result=StrategyResult(),
        )
    )

    assert report is not None

    assert report.summary.total_strategies == 0

    assert report.strategies == []