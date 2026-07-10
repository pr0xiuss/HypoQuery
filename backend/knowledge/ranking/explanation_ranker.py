from __future__ import annotations

from backend.knowledge.models.explanation import (
    Explanation,
)
from backend.knowledge.models.explanation_priority import (
    ExplanationPriority,
)


class ExplanationRanker:
    """
    Produces a deterministic ordering of explanation
    sections.
    """

    _ORDER = {
        ExplanationPriority.PRIMARY: 0,
        ExplanationPriority.SECONDARY: 1,
        ExplanationPriority.SUPPORTING: 2,
    }

    def rank(
        self,
        explanation: Explanation,
    ) -> Explanation:

        explanation.sections.sort(
            key=lambda section: (
                self._ORDER[
                    section.priority
                ],
                section.title,
            ),
        )

        return explanation