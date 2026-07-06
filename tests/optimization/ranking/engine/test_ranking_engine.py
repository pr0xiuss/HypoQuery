from backend.optimization.ranking.context import (
    RankingContext,
)
from backend.optimization.ranking.engine import (
    RankingEngine,
)
from backend.optimization.ranking.models.ranking_dimension import (
    RankingDimension,
)
from backend.optimization.ranking.models.score import (
    Score,
)
from backend.optimization.ranking.policy import (
    RankingPolicy,
)
from backend.optimization.ranking.registry.scorer_registry import (
    ScorerRegistry,
)
from backend.optimization.ranking.scorers.base_scorer import (
    RankingScorer,
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
from backend.optimization.recommendation.models.recommendation_result import (
    RecommendationResult,
)
from backend.optimization.validation.models.validation import (
    Validation,
)
from backend.optimization.validation.models.validation_result import (
    ValidationResult,
)
from backend.optimization.validation.models.validation_status import (
    ValidationStatus,
)


class DummyScorer(
    RankingScorer,
):

    @property
    def name(
        self,
    ) -> str:

        return "dummy"

    def score(
        self,
        context,
        recommendation,
        validation,
    ) -> Score:

        return Score(
            dimension=RankingDimension.IMPACT,
            score=100,
            reason="",
        )


def test_rank():

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

    recommendations = RecommendationResult()

    recommendations.recommendations.add(
        recommendation,
    )

    validations = ValidationResult()

    validations.validations.add(
        Validation(
            recommendation=recommendation,
            status=ValidationStatus.VALIDATED,
            validation_type=None,
            validation_artifact="",
            metrics=None,
        )
    )

    registry = ScorerRegistry()

    registry.register(
        DummyScorer(),
    )

    engine = RankingEngine(
        registry,
        RankingPolicy(),
    )

    result = engine.rank(
        RankingContext(
            recommendation_result=recommendations,
            validation_result=validations,
            fingerprint=None,
        )
    )

    assert len(result.rankings) == 1

    assert (
        result.rankings[0].scores[
            RankingDimension.IMPACT
        ].score
        == 100
    )