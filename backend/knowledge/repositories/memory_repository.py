from __future__ import annotations

from backend.knowledge.models.graph_snapshot import GraphSnapshot
from backend.knowledge.repositories.base_repository import (
    KnowledgeRepository,
)


class MemoryKnowledgeRepository(KnowledgeRepository):
    """
    In-memory KnowledgeGraph repository.

    Primarily used for testing and local execution.
    """

    def __init__(self) -> None:
        self.snapshot = GraphSnapshot()

    def save(
        self,
        graph: GraphSnapshot,
    ) -> None:
        self._graph = graph

    def load(self) -> GraphSnapshot | None:
        return self._graph