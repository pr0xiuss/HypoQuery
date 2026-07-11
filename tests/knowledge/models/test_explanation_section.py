from backend.knowledge.models.explanation_priority import (
    ExplanationPriority,
)
from backend.knowledge.models.explanation_section import (
    ExplanationSection,
)


def test_explanation_section():

    section = ExplanationSection(
        title="Recommendation",
        priority=ExplanationPriority.PRIMARY,
        content={
            "confidence": 0.95,
        },
    )

    assert (
        section.title
        == "Recommendation"
    )

    assert (
        section.priority
        == ExplanationPriority.PRIMARY
    )

    assert (
        section.content["confidence"]
        == 0.95
    )