from backend.knowledge.models.enums import (
    KnowledgeNodeType,
)
from backend.knowledge.models.graph_snapshot import (
    GraphSnapshot,
)
from backend.knowledge.models.knowledge_node import (
    KnowledgeNode,
)
from backend.knowledge.models.node_key import (
    NodeKey,
)
from backend.knowledge.retrieval.context import (
    RetrievalContext,
)
from backend.knowledge.retrieval.engine import (
    RetrievalEngine,
)
from backend.knowledge.retrieval.handlers.recommendation_retriever import (
    RecommendationRetriever,
)
from backend.knowledge.retrieval.job import (
    RetrievalJob,
)
from backend.knowledge.retrieval.objectives.objective_type import (
    ObjectiveType,
)
from backend.knowledge.retrieval.objectives.retrieval_objective import (
    RetrievalObjective,
)
from backend.knowledge.retrieval.registry.retrieval_registry import (
    RetrievalRegistry,
)
from backend.knowledge.retrieval.service import (
    RetrievalService,
)


def build_service() -> RetrievalService:

    registry = RetrievalRegistry()

    registry.register(
        RecommendationRetriever(),
    )

    return RetrievalService(
        engine=RetrievalEngine(
            registry,
        ),
    )


def build_context() -> RetrievalContext:

    graph = GraphSnapshot(
        nodes=(
            KnowledgeNode(
                key=NodeKey(
                    "recommendation:CREATE_INDEX",
                ),
                type=KnowledgeNodeType.RECOMMENDATION,
            ),
        ),
    )

    return RetrievalContext(
        job=RetrievalJob(
            graph=graph,
            objective=RetrievalObjective(
                type=ObjectiveType.FIND_RECOMMENDATIONS,
            ),
        ),
    )


def test_retrieval_is_deterministic():

    service = build_service()

    first = service.retrieve(
        build_context(),
    )

    second = service.retrieve(
        build_context(),
    )

    assert tuple(
        evidence.key
        for evidence in first
    ) == tuple(
        evidence.key
        for evidence in second
    )

    assert tuple(
        evidence.type
        for evidence in first
    ) == tuple(
        evidence.type
        for evidence in second
    )