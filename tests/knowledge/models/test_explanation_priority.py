from backend.knowledge.models.explanation_priority import (
    ExplanationPriority,
)


def test_explanation_priority():

    assert (
        ExplanationPriority.PRIMARY.value
        == "primary"
    )

    assert (
        ExplanationPriority.SECONDARY.value
        == "secondary"
    )

    assert (
        ExplanationPriority.SUPPORTING.value
        == "supporting"
    )