from __future__ import annotations

from backend.knowledge.models.knowledge_graph import (
    KnowledgeGraph,
)
from backend.knowledge.projection.context import (
    ProjectionContext,
)
from backend.knowledge.projection.registry.projection_registry import (
    ProjectionRegistry,
)


class ProjectionEngine:
    """
    Executes every registered projector against one
    optimization snapshot and builds a KnowledgeGraph.
    """

    def __init__(
        self,
        registry: ProjectionRegistry,
    ) -> None:
        self._registry = registry

    def project(
        self,
        context: ProjectionContext,
    ) -> KnowledgeGraph:

        graph = KnowledgeGraph()

        for projector in self._registry.all():

            projector.project(
                context=context,
                graph=graph,
            )

        return graph