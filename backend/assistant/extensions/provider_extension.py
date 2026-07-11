from __future__ import annotations

from backend.assistant.extensions.plugin import (
    Plugin,
)
from backend.assistant.providers.base_provider import (
    LanguageModel,
)
from backend.assistant.registry.provider_registry import (
    ProviderRegistry,
)


class ProviderExtension(
    Plugin,
):
    """
    Registers a language model provider
    with the assistant platform.
    """

    def __init__(
        self,
        name: str,
        provider: LanguageModel,
        registry: ProviderRegistry,
    ) -> None:

        self._name = name
        self._provider = provider
        self._registry = registry

    @property
    def name(
        self,
    ) -> str:

        return self._name

    def register(
        self,
    ) -> None:

        self._registry.register(
            self._name,
            self._provider,
        )