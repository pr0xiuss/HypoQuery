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
from backend.optimization.recommendation.rules.increase_work_mem_rule import (
    IncreaseWorkMemRule,
)


def create_context() -> RecommendationContext:

    result = AnalysisResult()

    result.findings.add(
        Finding(
            category=FindingCategory.EXECUTION,
            code="TEMP_DISK_WRITES",
            title="Temporary Disk Writes",
            description="Disk spill detected.",
            severity=FindingSeverity.HIGH,
        )
    )

    result.findings.add(
        Finding(
            category=FindingCategory.EXECUTION,
            code="EXPENSIVE_SORT",
            title="Expensive Sort",
            description="Sort operation is expensive.",
            severity=FindingSeverity.HIGH,
        )
    )

    return RecommendationContext(
        analysis_result=result,
    )


def test_increase_work_mem_rule():

    rule = IncreaseWorkMemRule()

    recommendations = rule.recommend(
        create_context(),
    )

    assert len(recommendations) == 1

    recommendation = list(recommendations)[0]

    assert recommendation.code == "INCREASE_WORK_MEM"