from backend.knowledge.models.context_priority import (
    ContextPriority,
)


def test_context_priority():

    assert (
        ContextPriority.PRIMARY.value
        == "primary"
    )

    assert (
        ContextPriority.SECONDARY.value
        == "secondary"
    )

    assert (
        ContextPriority.SUPPORTING.value
        == "supporting"
    )