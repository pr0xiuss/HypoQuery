from __future__ import annotations

from backend.assistant.renderers.base_renderer import (
    Renderer,
)
from backend.assistant.renderers.json_renderer import (
    JsonRenderer,
)
from backend.assistant.renderers.markdown_renderer import (
    MarkdownRenderer,
)


class RendererFactory:
    """
    Factory responsible for creating
    response renderers.
    """

    def create(
        self,
        name: str,
    ) -> Renderer:

        if name == "markdown":
            return MarkdownRenderer()

        if name == "json":
            return JsonRenderer()

        raise ValueError(
            f"Unknown renderer: {name}"
        )