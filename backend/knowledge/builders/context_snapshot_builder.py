from __future__ import annotations

from backend.knowledge.context_state.job import (
    ContextJob,
)
from backend.knowledge.models.context_metadata import (
    ContextMetadata,
)
from backend.knowledge.models.context_snapshot import (
    ContextSnapshot,
)
from backend.knowledge.models.optimization_context import (
    OptimizationContext,
)


class ContextSnapshotBuilder:
    """
    Builds immutable ContextSnapshots from assembled
    OptimizationContexts.
    """

    def build(
        self,
        job: ContextJob,
        context: OptimizationContext,
    ) -> ContextSnapshot:

        metadata = ContextMetadata(
            objective=job.objective.type.value,
            evidence_count=len(
                job.evidence,
            ),
            section_count=len(
                context.sections,
            ),
        )

        return ContextSnapshot(
            metadata=metadata,
            sections=tuple(
                context.sections,
            ),
            supporting_evidence=tuple(
                context.supporting_evidence,
            ),
        )