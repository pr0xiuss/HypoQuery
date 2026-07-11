from __future__ import annotations

from backend.knowledge.builders.context_snapshot_builder import (
    ContextSnapshotBuilder,
)
from backend.knowledge.builders.finding_context_builder import (
    FindingContextBuilder,
)
from backend.knowledge.builders.recommendation_context_builder import (
    RecommendationContextBuilder,
)
from backend.knowledge.builders.strategy_context_builder import (
    StrategyContextBuilder,
)
from backend.knowledge.builders.validation_context_builder import (
    ValidationContextBuilder,
)
from backend.knowledge.engine import (
    ContextEngine,
)
from backend.knowledge.registry.context_registry import (
    ContextRegistry,
)
from backend.knowledge.service import (
    ContextService,
)
from backend.knowledge.engine import (
    ExplanationEngine,
)
from backend.knowledge.explainers.explanation_builder import (
    ExplanationBuilder,
)
from backend.knowledge.explainers.finding_explainer import (
    FindingExplainer,
)
from backend.knowledge.explainers.recommendation_explainer import (
    RecommendationExplainer,
)
from backend.knowledge.explainers.strategy_explainer import (
    StrategyExplainer,
)
from backend.knowledge.explainers.summary_explainer import (
    SummaryExplainer,
)
from backend.knowledge.explainers.validation_explainer import (
    ValidationExplainer,
)
from backend.knowledge.registry.explanation_registry import (
    ExplanationRegistry,
)
from backend.knowledge.service import (
    ExplanationService,
)


def build_context_service() -> ContextService:
    """
    Builds the complete optimization context
    pipeline.
    """

    registry = ContextRegistry()

    registry.register(
        FindingContextBuilder(),
    )

    registry.register(
        RecommendationContextBuilder(),
    )

    registry.register(
        ValidationContextBuilder(),
    )

    registry.register(
        StrategyContextBuilder(),
    )

    engine = ContextEngine(
        registry=registry,
    )

    return ContextService(
        engine=engine,
        snapshot_builder=ContextSnapshotBuilder(),
    )


def build_explanation_service() -> ExplanationService:
    """
    Builds the complete explanation generation
    pipeline.
    """

    registry = ExplanationRegistry()

    registry.register(
        SummaryExplainer(),
    )

    registry.register(
        FindingExplainer(),
    )

    registry.register(
        RecommendationExplainer(),
    )

    registry.register(
        ValidationExplainer(),
    )

    registry.register(
        StrategyExplainer(),
    )

    engine = ExplanationEngine(
        registry=registry,
    )

    return ExplanationService(
        engine=engine,
        builder=ExplanationBuilder(),
    )