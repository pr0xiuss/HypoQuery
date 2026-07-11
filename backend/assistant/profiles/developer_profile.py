from __future__ import annotations

from backend.assistant.profiles.audience_profile import (
    AudienceProfile,
)
from backend.knowledge.models.explanation_snapshot import (
    ExplanationSnapshot,
)


class DeveloperProfile(
    AudienceProfile,
):
    """
    Presents the complete technical
    explanation.
    """

    @property
    def name(
        self,
    ) -> str:

        return "developer"

    def transform(
        self,
        explanation: ExplanationSnapshot,
    ) -> ExplanationSnapshot:

        return explanation