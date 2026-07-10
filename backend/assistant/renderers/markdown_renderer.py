from __future__ import annotations

from backend.assistant.models.ai_response import (
    AIResponse,
)
from backend.assistant.models.rendered_response import (
    RenderedResponse,
)


class MarkdownRenderer:
    """
    Renders AI responses as Markdown.
    """

    def render(
        self,
        response: AIResponse,
    ) -> RenderedResponse:

        return RenderedResponse(
            content=response.content,
            format="markdown",
        )