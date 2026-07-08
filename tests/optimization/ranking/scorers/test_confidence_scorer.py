from backend.optimization.ranking.scorers.confidence_scorer import (
    ConfidenceScorer,
)
from backend.optimization.recommendation.models.category import (
    RecommendationCategory,
)
from backend.optimization.recommendation.models.priority import (
    RecommendationPriority,
)
from backend.optimization.recommendation.models.recommendation import (
    Recommendation,
)
from backend.optimization.recommendation.models.recommendation_key import (
    RecommendationKey,
)
from backend.optimization.validation.models.validation import (
    Validation,
)
from backend.optimization.validation.models.validation_status import (
    ValidationStatus,
)


def test_confidence_score():

    scorer = ConfidenceScorer()

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

    score = scorer.score(
        context=None,
        recommendation=recommendation,
        validation=validation,
    )

    assert score.score == 100