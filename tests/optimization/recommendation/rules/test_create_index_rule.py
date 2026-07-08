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
from backend.optimization.recommendation.rules.create_index_rule import (
    CreateIndexRule,
)


def create_context() -> RecommendationContext:

    result = AnalysisResult()

    result.findings.add(
        Finding(
            category=FindingCategory.EXECUTION,
            code="LARGE_TABLE_SCAN",
            title="Large Sequential Scan",
            description="Large scan.",
            severity=FindingSeverity.HIGH,
        )
    )

    result.findings.add(
        Finding(
            category=FindingCategory.EXECUTION,
            code="HIGH_COST_NODE",
            title="High Cost",
            description="High cost.",
            severity=FindingSeverity.HIGH,
        )
    )

    return RecommendationContext(
        analysis_result=result,
    )


def test_create_index_rule():

    rule = CreateIndexRule()

    recommendations = rule.recommend(
        create_context(),
    )

    assert len(recommendations) == 1

    recommendation = list(recommendations)[0]

    assert recommendation.code == "CREATE_INDEX"