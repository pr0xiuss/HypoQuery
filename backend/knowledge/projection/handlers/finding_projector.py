from __future__ import annotations

from backend.knowledge.models.knowledge_graph import (
    KnowledgeGraph,
)
from backend.knowledge.projection.builders.finding_node_builder import (
    FindingNodeBuilder,
)
from backend.knowledge.projection.context import (
    ProjectionContext,
)
from backend.knowledge.projection.handlers.base_handler import (
    Projector,
)


class FindingProjector(Projector):
    """
    Projects deterministic Findings into the KnowledgeGraph.
    """

    @property
    def name(self) -> str:
        return "finding_projector"

    def __init__(self, node_builder: FindingNodeBuilder,) -> None:
        
        self._node_builder = node_builder

    def project(
        self,
        context: ProjectionContext,
        graph: KnowledgeGraph,
    ) -> None:

        for finding in context.job.execution.snapshot.findings:

            node = self._node_builder.build(
                finding,
            )

            graph.add_node(
                node,
            )
