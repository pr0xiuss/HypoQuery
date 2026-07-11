from backend.knowledge.filters.explanation_filter import (
    ExplanationFilter,
)
from backend.knowledge.models.explanation import (
    Explanation,
)
from backend.knowledge.models.explanation_priority import (
    ExplanationPriority,
)
from backend.knowledge.models.explanation_section import (
    ExplanationSection,
)


def test_explanation_filter():

    explanation = Explanation()

    explanation.add_section(
        ExplanationSection(
            title="Recommendation",
            priority=ExplanationPriority.PRIMARY,
        )
    )

    explanation.add_section(
        ExplanationSection(
            title="Strategy",
            priority=ExplanationPriority.SUPPORTING,
        )
    )

    sections = ExplanationFilter().by_priority(
        explanation,
        ExplanationPriority.PRIMARY,
    )

    assert len(
        sections,
    ) == 1

    assert (
        sections[0].title
        == "Recommendation"
    )