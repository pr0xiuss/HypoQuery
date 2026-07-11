from backend.knowledge.models.explanation import (
    Explanation,
)
from backend.knowledge.models.explanation_metadata import (
    ExplanationMetadata,
)
from backend.knowledge.models.explanation_snapshot import (
    ExplanationSnapshot,
)


def test_explanation_snapshot():

    explanation = Explanation()

    snapshot = ExplanationSnapshot(
        metadata=ExplanationMetadata(
            objective="find_recommendations",
            section_count=0,
        ),
        explanation=explanation,
    )

    assert (
        snapshot.metadata.objective
        == "find_recommendations"
    )

    assert (
        snapshot.explanation
        is explanation
    )