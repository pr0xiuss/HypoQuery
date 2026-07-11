from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from backend.assistant.models.ai_response import (
    AIResponse,
)
from backend.assistant.models.rendered_response import (
    RenderedResponse,
)


class Renderer(ABC):
    """
    Base contract implemented by every
    assistant renderer.
    """

    @abstractmethod
    def render(
        self,
        response: AIResponse,
    ) -> RenderedResponse:
        """
        Render an AI response into the
        desired output format.
        """