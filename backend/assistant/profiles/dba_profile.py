from __future__ import annotations

from backend.assistant.profiles.audience_profile import (
    AudienceProfile,
)
from backend.knowledge.models.explanation_snapshot import (
    ExplanationSnapshot,
)


class DBAProfile(
    AudienceProfile,
):
    """
    Presents explanations optimized for
    database administrators.
    """

    @property
    def name(
        self,
    ) -> str:

        return "dba"

    def transform(
        self,
        explanation: ExplanationSnapshot,
    ) -> ExplanationSnapshot:

        return explanation