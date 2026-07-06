from backend.optimization.ranking.context import (
    RankingContext,
)
from backend.optimization.ranking.models.ranking_dimension import (
    RankingDimension,
)
from backend.optimization.ranking.scorers.validation_scorer import (
    ValidationScorer,
)
from backend.optimization.validation.models.validation import (
    Validation,
)
from backend.optimization.validation.models.validation_status import (
    ValidationStatus,
)


def test_validated_score():

    scorer = ValidationScorer()

    score = scorer.score(
        context=None,
        recommendation=None,
        validation=Validation(
            recommendation=None,
            status=ValidationStatus.VALIDATED,
            validation_type=None,
            validation_artifact="",
            metrics=None,
        ),
    )

    assert (
        score.dimension
        == RankingDimension.VALIDATION
    )

    assert score.score == 100