from __future__ import annotations

from backend.assistant.profiles.rendering_profile import (
    RenderingProfile,
)


class JsonProfile(
    RenderingProfile,
):
    """
    JSON rendering profile.
    """

    @property
    def name(
        self,
    ) -> str:

        return "json"

    @property
    def renderer(
        self,
    ) -> str:

        return "json"