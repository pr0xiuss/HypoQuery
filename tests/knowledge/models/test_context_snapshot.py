from backend.knowledge.models.context_metadata import (
    ContextMetadata,
)
from backend.knowledge.models.context_priority import (
    ContextPriority,
)
from backend.knowledge.models.context_section import (
    ContextSection,
)
from backend.knowledge.models.context_snapshot import (
    ContextSnapshot,
)


def test_context_snapshot():

    snapshot = ContextSnapshot(
        metadata=ContextMetadata(
            objective="find_recommendations",
            evidence_count=2,
            section_count=1,
        ),
        sections=(
            ContextSection(
                title="Recommendation",
                priority=ContextPriority.PRIMARY,
            ),
        ),
        supporting_evidence=(),
    )

    assert (
        snapshot.metadata.objective
        == "find_recommendations"
    )

    assert len(
        snapshot.sections,
    ) == 1