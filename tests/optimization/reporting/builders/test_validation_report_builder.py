from backend.optimization.reporting.builders.validation_report_builder import (
    ValidationReportBuilder,
)
from backend.optimization.recommendation.models.category import (
    RecommendationCategory,
)
from backend.optimization.recommendation.models.recommendation_key import (
    RecommendationKey,
)
from backend.optimization.recommendation.models.priority import (
    RecommendationPriority,
)
from backend.optimization.recommendation.models.recommendation import (
    Recommendation,
)
from backend.optimization.validation.models.improvement_metrics import (
    ImprovementMetrics,
)
from backend.optimization.validation.models.validation import (
    Validation,
)
from backend.optimization.validation.models.validation_status import (
    ValidationStatus,
)
from backend.optimization.validation.models.validation_type import (
    ValidationType,
)


def test_build():

    recommendation = Recommendation(
        category=RecommendationCategory.INDEX,
        code="CREATE_INDEX",
        key=RecommendationKey(
            category="index",
            target="users",
            action="create",
        ),
        title="Create Index",
        description="",
        priority=RecommendationPriority.HIGH,
    )

    validation = Validation(
        recommendation=recommendation,
        status=ValidationStatus.VALIDATED,
        validation_type=ValidationType.HYPOTHETICAL_INDEX,
        validation_artifact="idx_users_email",
        metrics=ImprovementMetrics(
            before_cost=100,
            after_cost=20,
            cost_delta=-80,
            improvement_percent=80,
            before_rows=1000,
            after_rows=1000,
            plan_changed=True,
            cost_reduced=True,
        ),
    )

    builder = ValidationReportBuilder()

    report = builder.build(
        validation,
    )

    assert report.status == validation.status

    assert (
        report.validation_type
        == validation.validation_type
    )

    assert report.improvement_percent == 80

    assert report.plan_changed  