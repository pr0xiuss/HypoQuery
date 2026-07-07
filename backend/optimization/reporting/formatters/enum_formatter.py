from __future__ import annotations

from backend.optimization.recommendation.models.category import (
    RecommendationCategory,
)
from backend.optimization.recommendation.models.priority import (
    RecommendationPriority,
)
from backend.optimization.ranking.grouping.models.strategy_type import (
    StrategyType,
)
from backend.optimization.validation.models.validation_status import (
    ValidationStatus,
)
from backend.optimization.validation.models.validation_type import (
    ValidationType,
)


class EnumFormatter:
    """
    Formats domain enums for presentation.
    """

    def category(
        self,
        category: RecommendationCategory,
    ) -> str:

        return (
            category.value
            .replace("_", " ")
            .title()
        )

    def priority(
        self,
        priority: RecommendationPriority,
    ) -> str:

        return priority.name.title()

    def strategy(
        self,
        strategy: StrategyType,
    ) -> str:

        return (
            strategy.value
            .replace("_", " ")
            .title()
        )

    def validation_status(
        self,
        status: ValidationStatus | None,
    ) -> str:

        if status is None:

            return "N/A"

        return (
            status.value
            .replace("_", " ")
            .title()
        )

    def validation_type(
        self,
        validation_type: ValidationType | None,
    ) -> str:

        if validation_type is None:

            return "N/A"

        return (
            validation_type.value
            .replace("_", " ")
            .title()
        )