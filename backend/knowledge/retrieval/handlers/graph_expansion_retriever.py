from __future__ import annotations

from backend.knowledge.models.node_key import (
    NodeKey,
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
from backend.knowledge.retrieval.handlers.base_handler import (
    Retriever,
)
from backend.knowledge.models.enums import (
    KnowledgeNodeType,
)
from backend.knowledge.retrieval.evidence.evidence_type import (
    EvidenceType,
)
from backend.knowledge.retrieval.objectives.retrieval_scope import (
    RetrievalScope,
)
from backend.knowledge.retrieval.filters.graph_filter import (
    GraphFilter,
)

class GraphExpansionRetriever(Retriever):
    """
    Expands retrieved evidence by traversing neighbouring
    knowledge nodes.
    """
    def __init__(
        self,
        graph_filter: GraphFilter,
    ) -> None:

        self._graph_filter = graph_filter

    def retrieve(
        self,
        context: RetrievalContext,
        evidence: EvidenceSet,
    ) -> None:

        objective = context.job.objective

        if (
            objective.scope
            == RetrievalScope.LOCAL
        ):
            return

        graph = context.job.graph

        visited = context.visited

        for item in tuple(
            evidence,
        ):

            if item.key in visited:
                continue

            visited.add(
                item.key,
            )

            for node in self._graph_filter.neighbours(
                graph,
                item.key,
            ):

                if node.key in visited:
                    continue

                evidence.add(
                    Evidence(
                        key=node.key,
                        type=self._map_node_type(
                            node.type,
                        ),
                        source=EvidenceSource.KNOWLEDGE_GRAPH,
                    )
                )

                visited.add(
                    node.key,
                )


    @staticmethod
    def _map_node_type(
        node_type: KnowledgeNodeType,
    ) -> EvidenceType:

        mapping = {
            KnowledgeNodeType.FINDING:
                EvidenceType.FINDING,
            KnowledgeNodeType.RECOMMENDATION:
                EvidenceType.RECOMMENDATION,
            KnowledgeNodeType.VALIDATION:
                EvidenceType.VALIDATION,
            KnowledgeNodeType.STRATEGY:
                EvidenceType.STRATEGY,
            KnowledgeNodeType.EXECUTION:
                EvidenceType.EXECUTION,
        }

        return mapping.get(
            node_type,
            EvidenceType.GRAPH,
        )