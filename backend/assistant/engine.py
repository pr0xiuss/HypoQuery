from __future__ import annotations

from backend.assistant.assistant_context import (
    AssistantContext,
)
from backend.assistant.models.ai_response import (
    AIResponse,
)
from backend.assistant.registry.provider_registry import (
    ProviderRegistry,
)


class AssistantEngine:
    """
    Executes AI requests against the configured
    language model provider.
    """

    def __init__(
        self,
        registry: ProviderRegistry,
    ) -> None:

        self._registry = registry

    def generate(
        self,
        context: AssistantContext,
        provider: str,
    ) -> AIResponse:

        model = self._registry.get(
            provider,
        )

        response = model.generate(
            context.request,
        )

        context.response = response

        return response