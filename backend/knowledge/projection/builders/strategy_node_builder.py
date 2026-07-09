from __future__ import annotations

from backend.knowledge.models.enums import KnowledgeNodeType
from backend.knowledge.models.knowledge_node import KnowledgeNode
from backend.knowledge.models.node_key import NodeKey
from backend.knowledge.projection.builders.base_node_builder import (
    NodeBuilder,
)
from backend.optimization.ranking.grouping.models.strategy import (
    Strategy,
)


class StrategyNodeBuilder(NodeBuilder):
    """
    Builds KnowledgeNodes from optimization Strategies.
    """

    def build(
        self,
        strategy: Strategy,
    ) -> KnowledgeNode:

        return KnowledgeNode(
            key=NodeKey(
                value=f"strategy:{strategy.strategy_type.name}",
            ),
            type=KnowledgeNodeType.STRATEGY,
            properties={
                "strategy_type": strategy.strategy_type.name,
                "overall_score": strategy.overall_score,
                "representative": (
                    strategy.representative.recommendation.code
                ),
                "alternative_count": len(
                    strategy.alternatives,
                ),
            },
        )