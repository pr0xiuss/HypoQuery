from backend.knowledge.engine import (
    ExplanationEngine,
)
from backend.knowledge.explanation import (
    ExplanationContext,
)
from backend.knowledge.explanation_state.job import (
    ExplanationJob,
)
from backend.knowledge.explainers.recommendation_explainer import (
    RecommendationExplainer,
)
from backend.knowledge.models.context_metadata import (
    ContextMetadata,
)
from backend.knowledge.models.context_priority import (
    ContextPriority,
)
from backend.knowledge.models.context_section import (
    ContextSection,
)
from backend.knowledge.models.context_snapshot import (
    ContextSnapshot,
)
from backend.knowledge.models.explanation import (
    Explanation,
)
from backend.knowledge.registry.explanation_registry import (
    ExplanationRegistry,
)


def test_explanation_engine():

    registry = ExplanationRegistry()

    registry.register(
        RecommendationExplainer(),
    )

    engine = ExplanationEngine(
        registry,
    )

    context = ExplanationContext(
        job=ExplanationJob(
            context=ContextSnapshot(
                metadata=ContextMetadata(
                    objective="find_recommendations",
                    evidence_count=1,
                    section_count=1,
                ),
                sections=(
                    ContextSection(
                        title="Recommendation",
                        priority=ContextPriority.PRIMARY,
                    ),
                ),
                supporting_evidence=(),
            ),
            explanation=Explanation(),
        ),
    )

    explanation = engine.explain(
        context,
    )

    assert len(
        explanation.sections,
    ) == 1