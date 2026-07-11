from backend.knowledge.models.explanation import (
    Explanation,
)
from backend.knowledge.models.explanation_priority import (
    ExplanationPriority,
)
from backend.knowledge.models.explanation_section import (
    ExplanationSection,
)
from backend.knowledge.ranking.explanation_ranker import (
    ExplanationRanker,
)


def test_explanation_ranker():

    explanation = Explanation()

    explanation.add_section(
        ExplanationSection(
            title="Strategy",
            priority=ExplanationPriority.SUPPORTING,
        )
    )

    explanation.add_section(
        ExplanationSection(
            title="Recommendation",
            priority=ExplanationPriority.PRIMARY,
        )
    )

    explanation.add_section(
        ExplanationSection(
            title="Validation",
            priority=ExplanationPriority.SECONDARY,
        )
    )

    ExplanationRanker().rank(
        explanation,
    )

    assert (
        explanation.sections[0].priority
        == ExplanationPriority.PRIMARY
    )

    assert (
        explanation.sections[1].priority
        == ExplanationPriority.SECONDARY
    )

    assert (
        explanation.sections[2].priority
        == ExplanationPriority.SUPPORTING
    )