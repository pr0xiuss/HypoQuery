from backend.assistant.profiles.manager_profile import (
    ManagerProfile,
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


def test_manager_profile():

    snapshot = ExplanationSnapshot(
        metadata=ExplanationMetadata(
            objective="test",
            section_count=0,
        ),
        explanation=Explanation(),
    )

    profile = ManagerProfile()

    assert profile.name == "manager"

    assert (
        profile.transform(
            snapshot,
        )
        is snapshot
    )