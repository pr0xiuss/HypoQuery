from __future__ import annotations

from abc import ABC, abstractmethod

from backend.assistant.models.ai_request import (
    AIRequest,
)
from backend.assistant.models.ai_response import (
    AIResponse,
)


class LanguageModel(ABC):
    """
    Base contract implemented by every language
    model provider.
    """

    @abstractmethod
    def generate(
        self,
        request: AIRequest,
    ) -> AIResponse:
        """
        Generate a response for the supplied prompt.
        """