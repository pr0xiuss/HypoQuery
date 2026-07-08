from __future__ import annotations

from backend.optimization.ranking.grouping.models.strategy import (
    Strategy,
)
from backend.optimization.reporting.builders.recommendation_report_builder import (
    RecommendationReportBuilder,
)
from backend.optimization.reporting.builders.validation_report_builder import (
    ValidationReportBuilder,
)
from backend.optimization.reporting.models.strategy_report import (
    StrategyReport,
)


class StrategyReportBuilder:
    """
    Builds StrategyReport objects.
    """

    def __init__(
        self,
        recommendation_builder: RecommendationReportBuilder,
        validation_builder: ValidationReportBuilder,
    ) -> None:

        self._recommendation_builder = (
            recommendation_builder
        )

        self._validation_builder = (
            validation_builder
        )

    def build(
        self,
        strategy: Strategy,
    ) -> StrategyReport:

        representative = (
            strategy.representative
        )

        return StrategyReport(
            strategy=strategy.strategy_type,
            overall_score=strategy.overall_score,
            representative=(
                self._recommendation_builder.build(
                    representative.recommendation,
                    representative.validation,
                )
            ),
            validation=(
                self._validation_builder.build(
                    representative.validation,
                )
            ),
            alternatives=[
                self._recommendation_builder.build(
                    ranking.recommendation,
                    ranking.validation,
                )
                for ranking in strategy.alternatives
            ],
        )