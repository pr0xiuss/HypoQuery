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