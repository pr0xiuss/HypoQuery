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


def test_context_service():

    evidence = EvidenceSet()

    evidence.add(
        Evidence(
            key=NodeKey(
                "recommendation:CREATE_INDEX",
            ),
            type=EvidenceType.RECOMMENDATION,
            source=EvidenceSource.KNOWLEDGE_GRAPH,
        )
    )

    registry = ContextRegistry()

    registry.register(
        RecommendationContextBuilder(),
    )

    service = ContextService(
        engine=ContextEngine(
            registry,
        ),
        snapshot_builder=ContextSnapshotBuilder(),
    )

    snapshot = service.build(
        ContextContext(
            job=ContextJob(
                objective=RetrievalObjective(
                    type=ObjectiveType.FIND_RECOMMENDATIONS,
                ),
                evidence=evidence,
            ),
        ),
    )

    assert (
        snapshot.metadata.section_count
        == 1
    )