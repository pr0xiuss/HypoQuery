from __future__ import annotations

from backend.assistant.templates.prompt_template import (
    PromptTemplate,
)
from backend.knowledge.models.explanation_snapshot import (
    ExplanationSnapshot,
)


class OptimizationTemplate(
    PromptTemplate,
):
    """
    Default template used for optimization
    explanations.
    """

    def render(
        self,
        explanation: ExplanationSnapshot,
    ) -> str:

        report: list[str] = []

        report.append("# HypoQuery Optimization Report\n")

        report.append("## Summary")
        report.append(
            explanation.explanation.summary.title
        )
        report.append(
            explanation.explanation.summary.overview
        )

        report.append("\n## Metadata")
        report.append(
            f"- Objective: {explanation.metadata.objective}"
        )
        report.append(
            f"- Sections: {explanation.metadata.section_count}"
        )

        for section in explanation.explanation.sections:

            report.append(
                f"\n## {section.title}"
            )

            for key, value in section.content.items():

                report.append(
                    f"- {key.replace('_', ' ').title()}: {value}"
                )

        return "\n".join(report)