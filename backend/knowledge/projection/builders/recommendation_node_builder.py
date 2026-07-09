from __future__ import annotations

from backend.knowledge.models.enums import KnowledgeNodeType
from backend.knowledge.models.knowledge_node import KnowledgeNode
from backend.knowledge.models.node_key import NodeKey
from backend.knowledge.projection.builders.base_node_builder import (
    NodeBuilder,
)
from backend.optimization.recommendation.models.recommendation import (
    Recommendation,
)


class RecommendationNodeBuilder(NodeBuilder):
    """
    Builds KnowledgeNodes from Recommendations.
    """

    def build(
        self,
        recommendation: Recommendation,
    ) -> KnowledgeNode:

        return KnowledgeNode(
            key=NodeKey(
                value=f"recommendation:{recommendation.code}",
            ),
            type=KnowledgeNodeType.RECOMMENDATION,
            properties={
                "code": recommendation.code,
                "title": recommendation.title,
                "description": recommendation.description,
                "category": recommendation.category.name,
                "priority": recommendation.priority.name,
                "confidence": recommendation.confidence,
                "created_at": recommendation.created_at.isoformat(),
            },
        )