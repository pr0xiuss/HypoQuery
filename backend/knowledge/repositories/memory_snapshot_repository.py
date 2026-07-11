from __future__ import annotations

from backend.knowledge.models.graph_snapshot import GraphSnapshot
from backend.knowledge.repositories.snapshot_repository import (
    GraphSnapshotRepository,
)


class MemoryGraphSnapshotRepository(
    GraphSnapshotRepository,
):
    """
    In-memory GraphSnapshot repository.

    Used primarily for unit testing and local execution.
    """

    def __init__(self) -> None:
        self._snapshot: GraphSnapshot | None = None

    def save(
        self,
        snapshot: GraphSnapshot,
    ) -> None:
        self._snapshot = snapshot

    def load_latest(
        self,
    ) -> GraphSnapshot | None:
        return self._snapshot