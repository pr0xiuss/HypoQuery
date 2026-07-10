from backend.knowledge.engine import (
    ExplanationEngine,
)
from backend.knowledge.explanation import (
    ExplanationContext,
)
from backend.knowledge.explanation_state.job import (
    ExplanationJob,
)
from backend.knowledge.explainers.explanation_builder import (
    ExplanationBuilder,
)
from backend.knowledge.explainers.recommendation_explainer import (
    RecommendationExplainer,
)
from backend.knowledge.explainers.summary_explainer import (
    SummaryExplainer,
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
from backend.knowledge.service import (
    ExplanationService,
)


def test_explanation_pipeline():

    registry = ExplanationRegistry()

    registry.register(
        SummaryExplainer(),
    )

    registry.register(
        RecommendationExplainer(),
    )

    service = ExplanationService(
        engine=ExplanationEngine(
            registry,
        ),
        builder=ExplanationBuilder(),
    )

    snapshot = service.explain(
        ExplanationContext(
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
                            attributes={
                                "confidence": 1.0,
                            },
                        ),
                    ),
                    supporting_evidence=(),
                ),
                explanation=Explanation(),
            ),
        ),
    )

    assert (
        snapshot.metadata.section_count
        == 1
    )

    assert (
        snapshot.explanation.summary.title
        == "Optimization Explanation"
    )

    assert len(
        snapshot.explanation.sections
    ) == 1