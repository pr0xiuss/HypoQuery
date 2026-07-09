from __future__ import annotations

from abc import ABC, abstractmethod
from backend.knowledge.models.graph_snapshot import GraphSnapshot


class KnowledgeRepository(ABC):
    """
    Base contract for Knowledge Graph persistence.

    Repositories persist and retrieve complete graph
    projections. They never participate in projection
    logic itself.
    """

    @abstractmethod
    def save(
        self,
        snapshot: GraphSnapshot,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def load(self) -> GraphSnapshot | None:
        raise NotImplementedError