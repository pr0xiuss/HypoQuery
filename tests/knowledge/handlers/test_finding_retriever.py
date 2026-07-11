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
from backend.knowledge.retrieval.handlers.finding_retriever import (
    FindingRetriever,
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


def test_finding_retriever():

    graph = GraphSnapshot(
        nodes=(
            KnowledgeNode(
                key=NodeKey(
                    "finding:SEQ_SCAN",
                ),
                type=KnowledgeNodeType.FINDING,
            ),
        ),
    )

    context = RetrievalContext(
        job=RetrievalJob(
            graph=graph,
            objective=RetrievalObjective(
                type=ObjectiveType.FIND_SIMILAR_FINDINGS,
            ),
        ),
    )

    evidence = EvidenceSet()

    FindingRetriever().retrieve(
        context,
        evidence,
    )

    assert len(
        evidence,
    ) == 1