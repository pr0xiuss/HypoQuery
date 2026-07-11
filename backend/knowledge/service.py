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
from backend.knowledge.engine import (
    ExplanationEngine,
)
from backend.knowledge.explanation import (
    ExplanationContext,
)
from backend.knowledge.explainers.explanation_builder import (
    ExplanationBuilder,
)
from backend.knowledge.models.explanation_snapshot import (
    ExplanationSnapshot,
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
    

class ExplanationService:
    """
    Application service responsible for executing the
    complete explanation pipeline.
    """

    def __init__(
        self,
        engine: ExplanationEngine,
        builder: ExplanationBuilder,
    ) -> None:

        self._engine = engine

        self._builder = builder

    def explain(
        self,
        context: ExplanationContext,
    ) -> ExplanationSnapshot:

        explanation = self._engine.explain(
            context=context,
        )

        return self._builder.build(
            context.job,
            explanation,
        )