from backend.assistant.profiles.developer_profile import (
    DeveloperProfile,
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


def test_developer_profile():

    snapshot = ExplanationSnapshot(
        metadata=ExplanationMetadata(
            objective="test",
            section_count=0,
        ),
        explanation=Explanation(),
    )

    profile = DeveloperProfile()

    assert profile.name == "developer"

    assert (
        profile.transform(
            snapshot,
        )
        is snapshot
    )