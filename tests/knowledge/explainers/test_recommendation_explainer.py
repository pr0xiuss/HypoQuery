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
from backend.knowledge.models.explanation_priority import (
    ExplanationPriority,
)


def test_recommendation_explainer():

    snapshot = ContextSnapshot(
        metadata=ContextMetadata(
            objective="find_recommendations",
            evidence_count=1,
            section_count=1,
        ),
        sections=(
            ContextSection(
                title="Recommendation",
                priority=ContextPriority.PRIMARY,
                attributes={
                    "confidence": 1.0,
                },
            ),
        ),
        supporting_evidence=(),
    )

    explanation = Explanation()

    RecommendationExplainer().explain(
        ExplanationContext(
            job=ExplanationJob(
                context=snapshot,
                explanation=explanation,
            ),
        ),
        explanation,
    )

    assert len(
        explanation.sections,
    ) == 1

    assert (
        explanation.sections[0].priority
        == ExplanationPriority.PRIMARY
    )