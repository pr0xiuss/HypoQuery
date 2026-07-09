from __future__ import annotations

from backend.knowledge.models.enums import (
    KnowledgeNodeType,
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
from backend.knowledge.retrieval.handlers.base_handler import (
    Retriever,
)
from backend.knowledge.retrieval.objectives.objective_type import (
    ObjectiveType,
)

class RecommendationRetriever(Retriever):
    """
    Retrieves recommendation evidence from the
    Knowledge Graph.
    """

    def retrieve(
        self,
        context: RetrievalContext,
        evidence: EvidenceSet,
    ) -> None:

        objective = context.job.objective

        if (
            objective.type
            != ObjectiveType.FIND_RECOMMENDATIONS
        ):
            return

        graph = context.job.graph

        for node in graph.nodes:

            if (
                node.type
                != KnowledgeNodeType.RECOMMENDATION
            ):
                continue

            if (
                objective.target is not None
                and node.key.value
                != objective.target
            ):
                continue

            evidence.add(
                Evidence(
                    key=node.key,
                    type=EvidenceType.RECOMMENDATION,
                    source=EvidenceSource.KNOWLEDGE_GRAPH,
                )
            )