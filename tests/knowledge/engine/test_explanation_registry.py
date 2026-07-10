from backend.knowledge.explainers.recommendation_explainer import (
    RecommendationExplainer,
)
from backend.knowledge.registry.explanation_registry import (
    ExplanationRegistry,
)


def test_explanation_registry():

    registry = ExplanationRegistry()

    explainer = RecommendationExplainer()

    registry.register(
        explainer,
    )

    explainers = registry.all()

    assert len(
        explainers,
    ) == 1

    assert explainers[0] is explainer