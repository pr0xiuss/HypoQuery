from __future__ import annotations

from backend.assistant.profiles.audience_profile import (
    AudienceProfile,
)
from backend.knowledge.models.explanation_snapshot import (
    ExplanationSnapshot,
)


class ManagerProfile(
    AudienceProfile,
):
    """
    Presents explanations optimized for
    engineering managers.
    """

    @property
    def name(
        self,
    ) -> str:

        return "manager"

    def transform(
        self,
        explanation: ExplanationSnapshot,
    ) -> ExplanationSnapshot:

        return explanation