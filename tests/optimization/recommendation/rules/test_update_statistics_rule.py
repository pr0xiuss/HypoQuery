from backend.optimization.analysis.models.analysis_result import (
    AnalysisResult,
)
from backend.optimization.analysis.models.categories import (
    FindingCategory,
)
from backend.optimization.analysis.models.finding import (
    Finding,
)
from backend.optimization.analysis.models.severity import (
    FindingSeverity,
)
from backend.optimization.recommendation.context import (
    RecommendationContext,
)
from backend.optimization.recommendation.rules.update_statistics_rule import (
    UpdateStatisticsRule,
)


def create_context() -> RecommendationContext:

    result = AnalysisResult()

    result.findings.add(
        Finding(
            category=FindingCategory.EXECUTION,
            code="CARDINALITY_MISMATCH",
            title="Cardinality Mismatch",
            description="Planner estimates are inaccurate.",
            severity=FindingSeverity.HIGH,
        )
    )

    return RecommendationContext(
        analysis_result=result,
    )


def test_update_statistics_rule():

    rule = UpdateStatisticsRule()

    recommendations = rule.recommend(
        create_context(),
    )

    assert len(recommendations) == 1

    recommendation = list(recommendations)[0]

    assert recommendation.code == "UPDATE_STATISTICS"