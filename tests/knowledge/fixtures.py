from backend.optimization.analysis.models.categories import (
    FindingCategory,
)
from backend.optimization.analysis.models.finding import Finding
from backend.optimization.analysis.models.severity import (
    FindingSeverity,
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
from backend.optimization.validation.models.validation_type import (
    ValidationType,
)
from backend.optimization.ranking.grouping.models.strategy import (
    Strategy,
)
from backend.optimization.ranking.grouping.models.strategy_type import (
    StrategyType,
)
from backend.optimization.ranking.models.ranking import (
    Ranking,
)
from backend.optimization.ranking.models.ranking_dimension import (
    RankingDimension,
)
from backend.optimization.ranking.models.score import (
    Score,
)

def build_finding() -> Finding:

    return Finding(
        category=FindingCategory.EXECUTION,
        code="SEQ_SCAN",
        title="Sequential Scan",
        description="Table scan detected.",
        severity=FindingSeverity.HIGH,
    )

def build_recommendation() -> Recommendation:

    return Recommendation(
        category=RecommendationCategory.INDEX,
        code="CREATE_INDEX",
        key=RecommendationKey(
            category="index",
            target="users",
            action="create",
        ),
        title="Create Index",
        description="Create an index.",
        priority=RecommendationPriority.HIGH,
    )


def build_validation() -> Validation:

    return Validation(
        recommendation=build_recommendation(),
        status=ValidationStatus.VALIDATED,
        validation_type=ValidationType.HYPOTHETICAL_INDEX,
    )


def build_strategy() -> Strategy:

    recommendation = build_recommendation()

    ranking = Ranking(
        recommendation=recommendation,
        validation=None,
        scores={
            RankingDimension.IMPACT: Score(
                dimension=RankingDimension.IMPACT,
                score=10.0,
                reason="Test score",
            ),
        },
        total_score=10.0,
    )

    return Strategy(
        strategy_type=StrategyType.INDEXING,
        representative=ranking,
    )