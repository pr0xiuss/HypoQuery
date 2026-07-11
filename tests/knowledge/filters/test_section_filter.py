from backend.knowledge.filters.section_filter import (
    SectionFilter,
)
from backend.knowledge.models.explanation_priority import (
    ExplanationPriority,
)
from backend.knowledge.models.explanation_section import (
    ExplanationSection,
)


def test_section_filter():

    recommendation = ExplanationSection(
        title="Recommendation",
        priority=ExplanationPriority.PRIMARY,
    )

    strategy = ExplanationSection(
        title="Strategy",
        priority=ExplanationPriority.SUPPORTING,
    )

    sections = SectionFilter().by_priority(
        (
            recommendation,
            strategy,
        ),
        ExplanationPriority.PRIMARY,
    )

    assert len(
        sections,
    ) == 1

    assert (
        sections[0].title
        == "Recommendation"
    )