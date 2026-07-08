from backend.optimization.reporting.models.recommendation_report import (
    RecommendationReport,
)
from backend.optimization.recommendation.models.category import (
    RecommendationCategory,
)
from backend.optimization.recommendation.models.priority import (
    RecommendationPriority,
)


def test_recommendation_report():

    report = RecommendationReport(
        title="Create Index",
        description="Create an index on users(email).",
        category=RecommendationCategory.INDEX,
        priority=RecommendationPriority.HIGH,
        confidence=0.95,
        validated=True,
    )

    assert report.title == "Create Index"

    assert (
        report.category
        == RecommendationCategory.INDEX
    )

    assert (
        report.priority
        == RecommendationPriority.HIGH
    )

    assert report.confidence == 0.95

    assert report.validated