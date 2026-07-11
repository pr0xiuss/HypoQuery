from backend.knowledge.explanation_state.job import (
    ExplanationJob,
)
from backend.knowledge.explainers.explanation_builder import (
    ExplanationBuilder,
)
from backend.knowledge.models.context_metadata import (
    ContextMetadata,
)
from backend.knowledge.models.context_snapshot import (
    ContextSnapshot,
)
from backend.knowledge.models.explanation import (
    Explanation,
)


def test_explanation_builder():

    explanation = Explanation()

    snapshot = ExplanationBuilder().build(
        ExplanationJob(
            context=ContextSnapshot(
                metadata=ContextMetadata(
                    objective="find_recommendations",
                    evidence_count=1,
                    section_count=0,
                ),
                sections=(),
                supporting_evidence=(),
            ),
            explanation=explanation,
        ),
        explanation,
    )

    assert (
        snapshot.metadata.objective
        == "find_recommendations"
    )

    assert (
        snapshot.explanation
        is explanation
    )