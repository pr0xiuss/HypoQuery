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


def test_retrieval_pipeline():

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

    registry = RetrievalRegistry()

    registry.register(
        RecommendationRetriever(),
    )

    service = RetrievalService(
        engine=RetrievalEngine(
            registry,
        ),
    )

    evidence = service.retrieve(
        RetrievalContext(
            job=RetrievalJob(
                graph=graph,
                objective=RetrievalObjective(
                    type=ObjectiveType.FIND_RECOMMENDATIONS,
                ),
            ),
        ),
    )

    assert len(
        evidence,
    ) == 1

    assert (
        evidence.items[0].key.value
        == "recommendation:CREATE_INDEX"
    )