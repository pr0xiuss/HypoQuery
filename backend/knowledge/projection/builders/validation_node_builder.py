from __future__ import annotations

from backend.knowledge.models.enums import KnowledgeNodeType
from backend.knowledge.models.knowledge_node import KnowledgeNode
from backend.knowledge.models.node_key import NodeKey
from backend.knowledge.projection.builders.base_node_builder import (
    NodeBuilder,
)
from backend.optimization.validation.models.validation import (
    Validation,
)


class ValidationNodeBuilder(NodeBuilder):
    """
    Builds KnowledgeNodes from Validation results.
    """

    def build(
        self,
        validation: Validation,
    ) -> KnowledgeNode:

        return KnowledgeNode(
            key=NodeKey(
                value=f"validation:{validation.recommendation.code}",
            ),
            type=KnowledgeNodeType.VALIDATION,
            properties={
                "recommendation": validation.recommendation.code,
                "status": validation.status.name,
                "validation_type": validation.validation_type.name,
                "artifact": validation.validation_artifact,
                "validated_at": validation.validated_at.isoformat(),
                "improvement_percent": (
                    validation.metrics.improvement_percent
                ),
                "cost_delta": validation.metrics.cost_delta,
                "plan_changed": validation.metrics.plan_changed,
                "cost_reduced": validation.metrics.cost_reduced,
            },
        )