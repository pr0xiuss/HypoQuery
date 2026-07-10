from __future__ import annotations

from backend.assistant.models.ai_request import (
    AIRequest,
)
from backend.assistant.models.prompt import (
    Prompt,
)
from backend.assistant.prompts.base_prompt_builder import (
    PromptBuilder,
)
from backend.knowledge.models.explanation_snapshot import (
    ExplanationSnapshot,
)


class OptimizationPromptBuilder(
    PromptBuilder,
):
    """
    Builds prompts used to explain optimization
    reports.
    """

    def build(
        self,
        explanation: ExplanationSnapshot,
    ) -> AIRequest:

        report: list[str] = []

        report.append(
            "# Optimization Report\n"
        )

        report.append(
            "## Summary"
        )

        report.append(
            explanation.explanation.summary.title
        )

        if (
            explanation.explanation.summary.overview
        ):
            report.append(
                explanation.explanation.summary.overview
            )

        report.append(
            f"\nObjective: "
            f"{explanation.metadata.objective}"
        )

        report.append(
            f"Sections: "
            f"{explanation.metadata.section_count}"
        )

        for section in explanation.explanation.sections:

            report.append(
                f"\n## {section.title}"
            )

            for key, value in section.content.items():

                report.append(
                    f"- {key.replace('_', ' ').title()}: {value}"
                )

        prompt = Prompt(
            system=(
                "You are HypoQuery, an AI assistant specialized in "
                "explaining deterministic PostgreSQL optimization reports. "
                "The provided optimization report is the single source of truth. "
                "Your responsibility is to explain the report clearly and "
                "accurately using only the supplied information. "
                "Do not invent findings, recommendations, SQL statements, "
                "performance estimates, execution plans, or PostgreSQL features "
                "that are not explicitly provided. "
                "Do not speculate or fill in missing details from your own "
                "knowledge. If information is missing, explicitly state that "
                "HypoQuery did not provide enough information. "
                "Explain recommendations in concise, professional engineering "
                "language while preserving the intent and confidence of the "
                "original optimization report."
            ),
            user="\n".join(
                report,
            ),
        )

        return AIRequest(
            prompt=prompt,
        )