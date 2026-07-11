from backend.assistant.profiles.dba_profile import (
    DBAProfile,
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


def test_dba_profile():

    snapshot = ExplanationSnapshot(
        metadata=ExplanationMetadata(
            objective="test",
            section_count=0,
        ),
        explanation=Explanation(),
    )

    profile = DBAProfile()

    assert profile.name == "dba"

    assert (
        profile.transform(
            snapshot,
        )
        is snapshot
    )