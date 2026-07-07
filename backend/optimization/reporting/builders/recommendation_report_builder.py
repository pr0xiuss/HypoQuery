from __future__ import annotations

from backend.optimization.reporting.models.recommendation_report import (
    RecommendationReport,
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


class RecommendationReportBuilder:
    """
    Builds RecommendationReport objects.
    """

    def build(
        self,
        recommendation: Recommendation,
        validation: Validation | None,
    ) -> RecommendationReport:

        return RecommendationReport(
            title=recommendation.title,
            description=recommendation.description,
            category=recommendation.category,
            priority=recommendation.priority,
            confidence=recommendation.confidence,
            validated=(
                validation is not None
                and validation.status
                == ValidationStatus.VALIDATED
            ),
        )