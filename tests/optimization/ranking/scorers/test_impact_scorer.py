from backend.optimization.ranking.models.ranking_dimension import (
    RankingDimension,
)
from backend.optimization.ranking.scorers.impact_scorer import (
    ImpactScorer,
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


def test_impact_score():

    scorer = ImpactScorer()

    metrics = ImprovementMetrics(
        before_cost=100,
        after_cost=20,
        cost_delta=-80,
        improvement_percent=80,
        before_rows=1000,
        after_rows=1000,
        plan_changed=True,
        cost_reduced=True,
    )

    validation = Validation(
        recommendation=None,
        status=ValidationStatus.VALIDATED,
        validation_type=None,
        validation_artifact="",
        metrics=metrics,
    )

    score = scorer.score(
        context=None,
        recommendation=None,
        validation=validation,
    )

    assert (
        score.dimension
        == RankingDimension.IMPACT
    )

    assert score.score == 80