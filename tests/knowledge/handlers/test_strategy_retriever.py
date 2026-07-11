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
from backend.knowledge.retrieval.evidence.evidence_set import (
    EvidenceSet,
)
from backend.knowledge.retrieval.handlers.strategy_retriever import (
    StrategyRetriever,
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


def test_strategy_retriever():

    graph = GraphSnapshot(
        nodes=(
            KnowledgeNode(
                key=NodeKey(
                    "strategy:INDEXING",
                ),
                type=KnowledgeNodeType.STRATEGY,
            ),
        ),
    )

    context = RetrievalContext(
        job=RetrievalJob(
            graph=graph,
            objective=RetrievalObjective(
                type=ObjectiveType.FIND_STRATEGIES,
            ),
        ),
    )

    evidence = EvidenceSet()

    StrategyRetriever().retrieve(
        context,
        evidence,
    )

    assert len(
        evidence,
    ) == 1