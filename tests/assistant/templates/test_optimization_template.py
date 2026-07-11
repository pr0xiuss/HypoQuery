from backend.assistant.templates.optimization_template import (
    OptimizationTemplate,
)
from backend.knowledge.models.explanation import (
    Explanation,
)
from backend.knowledge.models.explanation_metadata import (
    ExplanationMetadata,
)
from backend.knowledge.models.explanation_priority import (
    ExplanationPriority,
)
from backend.knowledge.models.explanation_section import (
    ExplanationSection,
)
from backend.knowledge.models.explanation_snapshot import (
    ExplanationSnapshot,
)
from backend.knowledge.models.explanation_summary import (
    ExplanationSummary,
)


def test_optimization_template():

    explanation = Explanation()

    explanation.summary = ExplanationSummary(
        title="Optimization Report",
        overview="One recommendation found.",
    )

    explanation.add_section(
        ExplanationSection(
            title="Recommendation",
            priority=ExplanationPriority.PRIMARY,
            content={
                "action": "Create Index",
                "reason": "Sequential Scan",
            },
        )
    )

    snapshot = ExplanationSnapshot(
        metadata=ExplanationMetadata(
            objective="test",
            section_count=1,
        ),
        explanation=explanation,
    )

    body = OptimizationTemplate().render(
        snapshot,
    )

    assert "Optimization Report" in body

    assert "Recommendation" in body

    assert "Create Index" in body

    assert "Sequential Scan" in body