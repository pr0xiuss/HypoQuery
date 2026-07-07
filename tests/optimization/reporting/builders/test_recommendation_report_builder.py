from backend.optimization.reporting.builders.recommendation_report_builder import (
    RecommendationReportBuilder,
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
from backend.optimization.validation.models.validation import (
    Validation,
)
from backend.optimization.validation.models.validation_status import (
    ValidationStatus,
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
        validation_type=None,
        validation_artifact="",
        metrics=None,
    )

    builder = RecommendationReportBuilder()

    report = builder.build(
        recommendation,
        validation,
    )

    assert report.title == recommendation.title

    assert report.category == recommendation.category

    assert report.priority == recommendation.priority

    assert report.validated