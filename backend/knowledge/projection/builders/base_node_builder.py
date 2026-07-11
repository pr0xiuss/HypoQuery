from __future__ import annotations

from abc import ABC, abstractmethod

from backend.knowledge.models.knowledge_node import KnowledgeNode


class NodeBuilder(ABC):
    """
    Base contract for every KnowledgeNode builder.

    A NodeBuilder transforms one deterministic optimization
    artifact into a KnowledgeNode.
    """

    @abstractmethod
    def build(self, source: object,) -> KnowledgeNode:
        """
        Build a KnowledgeNode from a deterministic domain object.
        """
        raise NotImplementedError