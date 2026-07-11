from __future__ import annotations

from backend.assistant.providers.base_provider import (
    LanguageModel,
)
from backend.assistant.registry.provider_registry import (
    ProviderRegistry,
)


class ProviderFactory:
    """
    Factory responsible for resolving
    language model providers.
    """

    def __init__(
        self,
        registry: ProviderRegistry,
    ) -> None:

        self._registry = registry

    def create(
        self,
        name: str,
    ) -> LanguageModel:

        return self._registry.get(
            name,
        )