from __future__ import annotations

from backend.assistant.models.ai_request import (
    AIRequest,
)
from backend.assistant.models.ai_response import (
    AIResponse,
)
from backend.assistant.models.usage import (
    Usage,
)
from backend.assistant.providers.base_provider import (
    LanguageModel,
)


class MockProvider(LanguageModel):
    """
    Deterministic provider used during testing.
    """

    def generate(
        self,
        request: AIRequest,
    ) -> AIResponse:

        return AIResponse(
            content=(
                "Mock response generated."
            ),
            model="mock",
            usage=Usage(),
        )