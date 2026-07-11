from backend.knowledge.models.enums import (
    KnowledgeNodeType,
    KnowledgeRelationshipType,
)
from backend.knowledge.models.graph_snapshot import (
    GraphSnapshot,
)
from backend.knowledge.models.knowledge_node import (
    KnowledgeNode,
)
from backend.knowledge.models.knowledge_relationship import (
    KnowledgeRelationship,
)
from backend.knowledge.models.node_key import (
    NodeKey,
)
from backend.knowledge.models.relationship_key import (
    RelationshipKey,
)
from backend.knowledge.retrieval.context import (
    RetrievalContext,
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
from backend.knowledge.retrieval.handlers.graph_expansion_retriever import (
    GraphExpansionRetriever,
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
from backend.knowledge.retrieval.objectives.retrieval_scope import (
    RetrievalScope,
)
from backend.knowledge.retrieval.filters.graph_filter import (
    GraphFilter,
)
from backend.knowledge.retrieval.filters.node_filter import (
    NodeFilter,
)

def test_graph_expansion_retriever():

    recommendation = KnowledgeNode(
        key=NodeKey(
            "recommendation:CREATE_INDEX",
        ),
        type=KnowledgeNodeType.RECOMMENDATION,
    )

    validation = KnowledgeNode(
        key=NodeKey(
            "validation:CREATE_INDEX",
        ),
        type=KnowledgeNodeType.VALIDATION,
    )

    graph = GraphSnapshot(
        nodes=(
            recommendation,
            validation,
        ),
        relationships=(
            KnowledgeRelationship(
                key=RelationshipKey(
                    "r1",
                ),
                type=KnowledgeRelationshipType.VALIDATED_BY,
                source=recommendation.key,
                target=validation.key,
            ),
        ),
    )

    context = RetrievalContext(
        job=RetrievalJob(
            graph=graph,
            objective=RetrievalObjective(
                type=ObjectiveType.FIND_RECOMMENDATIONS,
                scope=RetrievalScope.NEIGHBOURHOOD,
            ),
        ),
    )

    evidence = EvidenceSet()

    evidence.add(
        Evidence(
            key=recommendation.key,
            type=EvidenceType.RECOMMENDATION,
            source=EvidenceSource.KNOWLEDGE_GRAPH,
        )
    )

    GraphExpansionRetriever(
        graph_filter=GraphFilter(
            node_filter=NodeFilter(),
        ),
    ).retrieve(
        context,
        evidence,
    )

    assert len(
        evidence,
    ) == 2