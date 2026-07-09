from __future__ import annotations

from backend.knowledge.models.graph_snapshot import GraphSnapshot
from backend.knowledge.projection.builders.graph_snapshot_builder import (
    GraphSnapshotBuilder,
)
from backend.knowledge.projection.context import ProjectionContext
from backend.knowledge.projection.engine import ProjectionEngine
from backend.knowledge.repositories.snapshot_repository import (
    GraphSnapshotRepository,
)


class KnowledgeProjectionService:
    """
    Application service responsible for executing the
    complete Knowledge Projection pipeline.

    OptimizationSnapshot
            ↓
    ProjectionEngine
            ↓
    KnowledgeGraph
            ↓
    GraphSnapshotBuilder
            ↓
    GraphSnapshotRepository
    """

    def __init__(
        self,
        engine: ProjectionEngine,
        snapshot_builder: GraphSnapshotBuilder,
        repository: GraphSnapshotRepository,
    ) -> None:
        self._engine = engine
        self._snapshot_builder = snapshot_builder
        self._repository = repository

    def project(
        self,
        context: ProjectionContext,
    ) -> GraphSnapshot:

        graph = self._engine.project(
            context=context,
        )

        snapshot = self._snapshot_builder.build(
            graph,
        )

        self._repository.save(
            snapshot,
        )

        return snapshot