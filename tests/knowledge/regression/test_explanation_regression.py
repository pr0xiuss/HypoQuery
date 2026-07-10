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


def build_service() -> ExplanationService:

    registry = ExplanationRegistry()

    registry.register(
        SummaryExplainer(),
    )

    registry.register(
        RecommendationExplainer(),
    )

    return ExplanationService(
        engine=ExplanationEngine(
            registry,
        ),
        builder=ExplanationBuilder(),
    )


def build_context() -> ExplanationContext:

    return ExplanationContext(
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
    )


def test_explanation_is_deterministic():

    service = build_service()

    first = service.explain(
        build_context(),
    )

    second = service.explain(
        build_context(),
    )

    assert (
        first.metadata.objective
        == second.metadata.objective
    )

    assert (
        first.metadata.section_count
        == second.metadata.section_count
    )

    assert (
        first.explanation.summary.title
        == second.explanation.summary.title
    )

    assert tuple(
        section.title
        for section in first.explanation.sections
    ) == tuple(
        section.title
        for section in second.explanation.sections
    )