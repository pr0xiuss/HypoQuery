from __future__ import annotations

from backend.assistant.profiles.rendering_profile import (
    RenderingProfile,
)


class MarkdownProfile(
    RenderingProfile,
):
    """
    Markdown rendering profile.
    """

    @property
    def name(
        self,
    ) -> str:

        return "markdown"

    @property
    def renderer(
        self,
    ) -> str:

        return "markdown"