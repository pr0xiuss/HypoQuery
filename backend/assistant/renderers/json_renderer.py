from __future__ import annotations

import json

from backend.assistant.models.ai_response import (
    AIResponse,
)
from backend.assistant.models.rendered_response import (
    RenderedResponse,
)
from backend.assistant.renderers.base_renderer import Renderer

class JsonRenderer(Renderer):
    """
    Renders AI responses as JSON.
    """

    def render(
        self,
        response: AIResponse,
    ) -> RenderedResponse:

        return RenderedResponse(
            content=json.dumps(
                {
                    "model": response.model,
                    "response": response.content,
                    "usage": {
                        "input_tokens": (
                            response.usage.input_tokens
                        ),
                        "output_tokens": (
                            response.usage.output_tokens
                        ),
                        "total_tokens": (
                            response.usage.total_tokens
                        ),
                    },
                },
                indent=2,
            ),
            format="json",
        )