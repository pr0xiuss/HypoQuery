from backend.optimization.reporting.formatters.enum_formatter import (
    EnumFormatter,
)
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


def test_format_enums():

    formatter = EnumFormatter()

    assert (
        formatter.category(
            RecommendationCategory.INDEX,
        )
        == "Index"
    )

    assert (
        formatter.priority(
            RecommendationPriority.HIGH,
        )
        == "High"
    )

    assert (
        formatter.strategy(
            StrategyType.QUERY_REWRITE,
        )
        == "Query Rewrite"
    )

    assert (
        formatter.validation_status(
            ValidationStatus.VALIDATED,
        )
        == "Validated"
    )

    assert (
        formatter.validation_type(
            ValidationType.HYPOTHETICAL_INDEX,
        )
        == "Hypothetical Index"
    )