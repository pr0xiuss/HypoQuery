from backend.knowledge.builders.context_snapshot_builder import (
    ContextSnapshotBuilder,
)
from backend.knowledge.context_state.job import (
    ContextJob,
)
from backend.knowledge.models.context_priority import (
    ContextPriority,
)
from backend.knowledge.models.context_section import (
    ContextSection,
)
from backend.knowledge.models.optimization_context import (
    OptimizationContext,
)
from backend.knowledge.retrieval.evidence.evidence_set import (
    EvidenceSet,
)
from backend.knowledge.retrieval.objectives.objective_type import (
    ObjectiveType,
)
from backend.knowledge.retrieval.objectives.retrieval_objective import (
    RetrievalObjective,
)


def test_context_snapshot_builder():

    context = OptimizationContext()

    context.add_section(
        ContextSection(
            title="Recommendation",
            priority=ContextPriority.PRIMARY,
        )
    )

    snapshot = ContextSnapshotBuilder().build(
        ContextJob(
            objective=RetrievalObjective(
                type=ObjectiveType.FIND_RECOMMENDATIONS,
            ),
            evidence=EvidenceSet(),
        ),
        context,
    )

    assert (
        snapshot.metadata.section_count
        == 1
    )

    assert len(
        snapshot.sections,
    ) == 1