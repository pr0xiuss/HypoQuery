from __future__ import annotations

from backend.knowledge.models.knowledge_graph import (
    KnowledgeGraph,
)
from backend.knowledge.projection.builders.recommendation_node_builder import (
    RecommendationNodeBuilder,
)
from backend.knowledge.projection.builders.recommendation_relationship_builder import (
    RecommendationRelationshipBuilder,
)
from backend.knowledge.projection.context import (
    ProjectionContext,
)
from backend.knowledge.projection.handlers.base_handler import (
    Projector,
)


class RecommendationProjector(Projector):
    """
    Projects deterministic Recommendations into the
    KnowledgeGraph.
    """

    @property
    def name(self) -> str:
        return "recommendation_projector"

    def __init__(
        self,
        node_builder: RecommendationNodeBuilder,
        relationship_builder: RecommendationRelationshipBuilder,
    ) -> None:
        self._node_builder = node_builder
        self._relationship_builder = relationship_builder

    def project(
        self,
        context: ProjectionContext,
        graph: KnowledgeGraph,
    ) -> None:

        for recommendation in context.job.execution.snapshot.recommendations:

            node = self._node_builder.build(
                recommendation,
            )

            graph.add_node(
                node,
            )

            relationships = self._relationship_builder.build(
                recommendation,
                graph,
            )

            for relationship in relationships:

                graph.connect(
                    relationship,
                )