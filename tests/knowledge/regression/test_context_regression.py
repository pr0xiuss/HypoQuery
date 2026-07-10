from backend.knowledge.builders.context_snapshot_builder import (
    ContextSnapshotBuilder,
)
from backend.knowledge.builders.recommendation_context_builder import (
    RecommendationContextBuilder,
)
from backend.knowledge.context import (
    ContextContext,
)
from backend.knowledge.context_state.job import (
    ContextJob,
)
from backend.knowledge.engine import (
    ContextEngine,
)
from backend.knowledge.models.node_key import (
    NodeKey,
)
from backend.knowledge.registry.context_registry import (
    ContextRegistry,
)
from backend.knowledge.retrieval.evidence.evidence import (
    Evidence,
)
from backend.knowledge.retrieval.evidence.evidence_set import (
    EvidenceSet,
)
from backend.knowledge.retrieval.evidence.evidence_source import (
    EvidenceSource,
)
from backend.knowledge.retrieval.evidence.evidence_type import (
    EvidenceType,
)
from backend.knowledge.retrieval.objectives.objective_type import (
    ObjectiveType,
)
from backend.knowledge.retrieval.objectives.retrieval_objective import (
    RetrievalObjective,
)
from backend.knowledge.service import (
    ContextService,
)


def build_service() -> ContextService:

    registry = ContextRegistry()

    registry.register(
        RecommendationContextBuilder(),
    )

    return ContextService(
        engine=ContextEngine(
            registry,
        ),
        snapshot_builder=ContextSnapshotBuilder(),
    )


def build_context() -> ContextContext:

    evidence = EvidenceSet()

    evidence.add(
        Evidence(
            key=NodeKey(
                "recommendation:CREATE_INDEX",
            ),
            type=EvidenceType.RECOMMENDATION,
            source=EvidenceSource.KNOWLEDGE_GRAPH,
            confidence=0.95,
        )
    )

    return ContextContext(
        job=ContextJob(
            objective=RetrievalObjective(
                type=ObjectiveType.FIND_RECOMMENDATIONS,
            ),
            evidence=evidence,
        ),
    )


def test_context_is_deterministic():

    service = build_service()

    first = service.build(
        build_context(),
    )

    second = service.build(
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

    assert tuple(
        section.title
        for section in first.sections
    ) == tuple(
        section.title
        for section in second.sections
    )