from backend.knowledge.explanation import (
    ExplanationContext,
)
from backend.knowledge.explanation_state.job import (
    ExplanationJob,
)
from backend.knowledge.explainers.summary_explainer import (
    SummaryExplainer,
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


def test_summary_explainer():

    snapshot = ContextSnapshot(
        metadata=ContextMetadata(
            objective="find_recommendations",
            evidence_count=1,
            section_count=0,
        ),
        sections=(),
        supporting_evidence=(),
    )

    explanation = Explanation()

    SummaryExplainer().explain(
        ExplanationContext(
            job=ExplanationJob(
                context=snapshot,
                explanation=explanation,
            ),
        ),
        explanation,
    )

    assert (
        explanation.summary.title
        == "Optimization Explanation"
    )