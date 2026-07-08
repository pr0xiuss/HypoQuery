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
from backend.optimization.recommendation.engine import (
    RecommendationEngine,
)
from backend.optimization.recommendation.registry.rule_registry import (
    RecommendationRuleRegistry,
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

    return RecommendationContext(
        analysis_result=result,
    )


def test_engine_runs_registered_rules():

    registry = RecommendationRuleRegistry()

    registry.register(
        CreateIndexRule(),
    )

    engine = RecommendationEngine(
        registry,
    )

    result = engine.recommend(
        create_context(),
    )

    assert result.total_recommendations == 1


def test_engine_returns_empty_when_no_rules():

    engine = RecommendationEngine(
        RecommendationRuleRegistry(),
    )

    result = engine.recommend(
        create_context(),
    )

    assert result.total_recommendations == 0