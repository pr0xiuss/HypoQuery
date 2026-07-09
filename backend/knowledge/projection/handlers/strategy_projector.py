from __future__ import annotations

from backend.knowledge.models.knowledge_graph import (
    KnowledgeGraph,
)
from backend.knowledge.projection.builders.strategy_node_builder import (
    StrategyNodeBuilder,
)
from backend.knowledge.projection.builders.strategy_relationship_builder import (
    StrategyRelationshipBuilder,
)
from backend.knowledge.projection.context import (
    ProjectionContext,
)
from backend.knowledge.projection.handlers.base_handler import (
    Projector,
)


class StrategyProjector(Projector):
    """
    Projects optimization Strategies into the KnowledgeGraph.
    """

    @property
    def name(self) -> str:
        return "strategy_projector"

    def __init__(
        self,
        node_builder: StrategyNodeBuilder,
        relationship_builder: StrategyRelationshipBuilder,
    ) -> None:
        self._node_builder = node_builder
        self._relationship_builder = relationship_builder

    def project(
        self,
        context: ProjectionContext,
        graph: KnowledgeGraph,
    ) -> None:

        for strategy in context.job.execution.snapshot.strategies:

            node = self._node_builder.build(
                strategy,
            )

            graph.add_node(
                node,
            )

            relationships = self._relationship_builder.build(
                strategy,
                graph,
            )

            for relationship in relationships:

                graph.connect(
                    relationship,
                )