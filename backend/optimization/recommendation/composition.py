from __future__ import annotations

from backend.optimization.recommendation.engine import (
    RecommendationEngine,
)
from backend.optimization.recommendation.registry.rule_registry import (
    RecommendationRuleRegistry,
)
from backend.optimization.recommendation.rules.create_index_rule import (
    CreateIndexRule,
)
from backend.optimization.recommendation.rules.increase_work_mem_rule import (
    IncreaseWorkMemRule,
)
from backend.optimization.recommendation.rules.update_statistics_rule import (
    UpdateStatisticsRule,
)


def build_recommendation_engine() -> RecommendationEngine:
    """
    Composition root for the Recommendation bounded context.
    """

    registry = RecommendationRuleRegistry()

    registry.register(
        CreateIndexRule(),
    )

    registry.register(
        UpdateStatisticsRule(),
    )

    registry.register(
        IncreaseWorkMemRule(),
    )

    return RecommendationEngine(
        registry,
    )