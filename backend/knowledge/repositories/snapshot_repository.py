from __future__ import annotations

from abc import ABC, abstractmethod

from backend.knowledge.models.graph_snapshot import GraphSnapshot


class GraphSnapshotRepository(ABC):
    """
    Base contract for GraphSnapshot persistence.

    GraphSnapshots represent immutable knowledge projections
    and may be persisted for replay, comparison, auditing,
    or historical analysis.
    """

    @abstractmethod
    def save(
        self,
        snapshot: GraphSnapshot,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def load_latest(
        self,
    ) -> GraphSnapshot | None:
        raise NotImplementedError