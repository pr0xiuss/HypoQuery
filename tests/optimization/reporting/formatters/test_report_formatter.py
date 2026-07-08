from backend.optimization.reporting.formatters.enum_formatter import (
    EnumFormatter,
)
from backend.optimization.reporting.formatters.report_formatter import (
    ReportFormatter,
)
from backend.optimization.reporting.formatters.value_formatter import (
    ValueFormatter,
)
from backend.optimization.recommendation.models.category import (
    RecommendationCategory,
)
from backend.optimization.recommendation.models.priority import (
    RecommendationPriority,
)


def test_report_formatter():

    formatter = ReportFormatter(
        ValueFormatter(),
        EnumFormatter(),
    )

    assert (
        formatter.percentage(
            50,
        )
        == "50.0%"
    )

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
        formatter.boolean(
            True,
        )
        == "Yes"
    )