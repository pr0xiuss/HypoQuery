from backend.knowledge.models.context_priority import (
    ContextPriority,
)
from backend.knowledge.models.context_section import (
    ContextSection,
)


def test_context_section():

    section = ContextSection(
        title="Recommendation",
        priority=ContextPriority.PRIMARY,
        attributes={
            "confidence": 0.95,
        },
    )

    assert (
        section.title
        == "Recommendation"
    )

    assert (
        section.priority
        == ContextPriority.PRIMARY
    )

    assert (
        section.attributes["confidence"]
        == 0.95
    )