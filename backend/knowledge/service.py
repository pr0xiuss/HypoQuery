from __future__ import annotations

from backend.knowledge.context import (
    ContextContext,
)
from backend.knowledge.engine import (
    ContextEngine,
)
from backend.knowledge.models.context_snapshot import (
    ContextSnapshot,
)
from backend.knowledge.builders.context_snapshot_builder import (
    ContextSnapshotBuilder,
)


class ContextService:
    """
    Application service responsible for executing the
    complete Context Building pipeline.

    EvidenceSet
          ↓
    ContextEngine
          ↓
    OptimizationContext
          ↓
    ContextSnapshotBuilder
          ↓
    ContextSnapshot
    """

    def __init__(
        self,
        engine: ContextEngine,
        snapshot_builder: ContextSnapshotBuilder,
    ) -> None:

        self._engine = engine

        self._snapshot_builder = snapshot_builder

    def build(
        self,
        context: ContextContext,
    ) -> ContextSnapshot:

        optimization_context = self._engine.build(
            context=context,
        )

        return self._snapshot_builder.build(
            context.job,
            optimization_context,
        )