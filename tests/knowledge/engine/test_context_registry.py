from backend.knowledge.builders.recommendation_context_builder import (
    RecommendationContextBuilder,
)
from backend.knowledge.registry.context_registry import (
    ContextRegistry,
)


def test_context_registry():

    registry = ContextRegistry()

    builder = RecommendationContextBuilder()

    registry.register(
        builder,
    )

    builders = registry.all()

    assert len(
        builders,
    ) == 1

    assert builders[0] is builder