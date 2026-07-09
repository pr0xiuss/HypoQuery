from __future__ import annotations

from backend.knowledge.models.enums import KnowledgeNodeType
from backend.knowledge.models.knowledge_node import KnowledgeNode
from backend.knowledge.models.node_key import NodeKey
from backend.knowledge.projection.builders.base_node_builder import (
    NodeBuilder,
)
from backend.optimization.analysis.models.finding import Finding


class FindingNodeBuilder(NodeBuilder):
    """
    Builds KnowledgeNodes from Findings.
    """

    def build(
        self,
        finding: Finding,
    ) -> KnowledgeNode:

        return KnowledgeNode(
            key=NodeKey(
                value=f"finding:{finding.code}",
            ),
            type=KnowledgeNodeType.FINDING,
            properties={
                "code": finding.code,
                "title": finding.title,
                "description": finding.description,
                "category": finding.category.name,
                "severity": finding.severity.name,
                "observed_at": finding.observed_at.isoformat(),
            },
        )