from __future__ import annotations

from backend.optimization.reporting.formatters.enum_formatter import EnumFormatter
from backend.optimization.reporting.formatters.value_formatter import ValueFormatter
from backend.optimization.recommendation.models.category import RecommendationCategory
from backend.optimization.recommendation.models.priority import RecommendationPriority
from backend.optimization.ranking.grouping.models.strategy_type import StrategyType
from backend.optimization.validation.models.validation_status import ValidationStatus
from backend.optimization.validation.models.validation_type import ValidationType


class ReportFormatter:
    """
    Facade over report formatting services.
    """

    def __init__(
        self,
        value_formatter: ValueFormatter,
        enum_formatter: EnumFormatter,
    ) -> None:

        self._value = value_formatter
        self._enum = enum_formatter

    def percentage(
        self,
        value: float,
    ) -> str:

        return self._value.percentage(
            value,
        )

    def score(
        self,
        value: float,
    ) -> str:

        return self._value.score(
            value,
        )

    def boolean(
        self,
        value: bool,
    ) -> str:

        return self._value.boolean(
            value,
        )

    def cost(
        self,
        value: float,
    ) -> str:

        return self._value.cost(
            value,
        )

    def duration_ms(
        self,
        value: float,
    ) -> str:

        return self._value.duration_ms(
            value,
        )

    def category(
        self,
        category: RecommendationCategory,
    ) -> str:

        return self._enum.category(
            category,
        )

    def priority(
        self,
        priority: RecommendationPriority,
    ) -> str:

        return self._enum.priority(
            priority,
        )

    def strategy(
        self,
        strategy: StrategyType,
    ) -> str:

        return self._enum.strategy(
            strategy,
        )

    def validation_status(
        self,
        status: ValidationStatus | None,
    ) -> str:

        return self._enum.validation_status(
            status,
        )

    def validation_type(
        self,
        validation_type: ValidationType | None,
    ) -> str:

        return self._enum.validation_type(
            validation_type,
        )