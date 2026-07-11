from __future__ import annotations

from backend.knowledge.explainers.base_explainer import (
    Explainer,
)
from backend.knowledge.explanation import (
    ExplanationContext,
)
from backend.knowledge.models.explanation import (
    Explanation,
)
from backend.knowledge.models.explanation_summary import (
    ExplanationSummary,
)


class SummaryExplainer(Explainer):
    """
    Produces the high-level explanation summary.
    """

    def explain(
        self,
        context: ExplanationContext,
        explanation: Explanation,
    ) -> None:

        explanation.summary = ExplanationSummary(
            title="Optimization Explanation",
            overview=(
                f"{len(context.job.context.sections)} "
                "explanation sections generated."
            ),
            confidence=1.0,
        )