from backend.knowledge.models.explanation import (
    Explanation,
)
from backend.knowledge.models.explanation_priority import (
    ExplanationPriority,
)
from backend.knowledge.models.explanation_section import (
    ExplanationSection,
)
from backend.knowledge.models.explanation_summary import (
    ExplanationSummary,
)


def test_explanation():

    explanation = Explanation()

    explanation.summary = ExplanationSummary(
        title="Optimization",
    )

    explanation.add_section(
        ExplanationSection(
            title="Recommendation",
            priority=ExplanationPriority.PRIMARY,
        )
    )

    assert (
        explanation.summary.title
        == "Optimization"
    )

    assert len(
        explanation.sections,
    ) == 1