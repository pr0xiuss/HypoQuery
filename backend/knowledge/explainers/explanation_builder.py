from __future__ import annotations

from backend.knowledge.explanation_state.job import (
    ExplanationJob,
)
from backend.knowledge.models.explanation import (
    Explanation,
)
from backend.knowledge.models.explanation_metadata import (
    ExplanationMetadata,
)
from backend.knowledge.models.explanation_snapshot import (
    ExplanationSnapshot,
)


class ExplanationBuilder:
    """
    Builds immutable ExplanationSnapshots from
    generated Explanations.
    """

    def build(
        self,
        job: ExplanationJob,
        explanation: Explanation,
    ) -> ExplanationSnapshot:

        metadata = ExplanationMetadata(
            objective=(
                job.context.metadata.objective
            ),
            section_count=len(
                explanation.sections,
            ),
        )

        return ExplanationSnapshot(
            metadata=metadata,
            explanation=explanation,
        )