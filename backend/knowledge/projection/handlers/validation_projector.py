from __future__ import annotations

from backend.knowledge.models.knowledge_graph import (
    KnowledgeGraph,
)
from backend.knowledge.projection.builders.validation_node_builder import (
    ValidationNodeBuilder,
)
from backend.knowledge.projection.builders.validation_relationship_builder import (
    ValidationRelationshipBuilder,
)
from backend.knowledge.projection.context import (
    ProjectionContext,
)
from backend.knowledge.projection.handlers.base_handler import (
    Projector,
)


class ValidationProjector(Projector):
    """
    Projects Validation results into the KnowledgeGraph.
    """

    @property
    def name(self) -> str:
        return "validation_projector"

    def __init__(
        self,
        node_builder: ValidationNodeBuilder,
        relationship_builder: ValidationRelationshipBuilder,
    ) -> None:
        self._node_builder = node_builder
        self._relationship_builder = relationship_builder

    def project(
        self,
        context: ProjectionContext,
        graph: KnowledgeGraph,
    ) -> None:

        for validation in context.job.execution.snapshot.validations:

            node = self._node_builder.build(
                validation,
            )

            graph.add_node(
                node,
            )

            relationships = self._relationship_builder.build(
                validation,
                graph,
            )

            for relationship in relationships:

                graph.add_relationship(
                    relationship,
                )