from backend.assistant.prompts.optimization_prompt_builder import (
    OptimizationPromptBuilder,
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


def test_optimization_prompt_builder():

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
            objective="find_recommendations",
            section_count=1,
        ),
        explanation=explanation,
    )

    request = (
        OptimizationPromptBuilder().build(
            snapshot,
        )
    )

    assert "HypoQuery" in request.prompt.system

    assert (
        "Optimization Report"
        in request.prompt.user
    )

    assert (
        "Create Index"
        in request.prompt.user
    )