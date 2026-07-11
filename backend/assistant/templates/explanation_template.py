from __future__ import annotations

from backend.assistant.templates.prompt_template import (
    PromptTemplate,
)
from backend.knowledge.models.explanation_snapshot import (
    ExplanationSnapshot,
)


class ExplanationTemplate(
    PromptTemplate,
):
    """
    Generic explanation template.

    Can be specialized in the future for
    different explanation styles.
    """

    def render(
        self,
        explanation: ExplanationSnapshot,
    ) -> str:

        return (
            explanation.explanation.summary.overview
        )