from backend.optimization.reporting.models.recommendation_report import (
    RecommendationReport,
)
from backend.optimization.reporting.models.strategy_report import (
    StrategyReport,
)
from backend.optimization.reporting.models.validation_report import (
    ValidationReport,
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


def test_strategy_report():

    recommendation = RecommendationReport(
        title="Create Index",
        description="",
        category=RecommendationCategory.INDEX,
        priority=RecommendationPriority.HIGH,
        confidence=0.95,
        validated=True,
    )

    validation = ValidationReport(
        status=ValidationStatus.VALIDATED,
        validation_type=ValidationType.HYPOTHETICAL_INDEX,
        improvement_percent=81.4,
        cost_before=120,
        cost_after=25,
        plan_changed=True,
    )

    report = StrategyReport(
        strategy=StrategyType.INDEXING,
        overall_score=92.5,
        representative=recommendation,
        validation=validation,
    )

    assert (
        report.strategy
        == StrategyType.INDEXING
    )

    assert report.overall_score == 92.5

    assert (
        report.representative
        == recommendation
    )

    assert (
        report.validation
        == validation
    )

    assert report.alternatives == []