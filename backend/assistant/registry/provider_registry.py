from __future__ import annotations

from backend.assistant.providers.base_provider import (
    LanguageModel,
)


class ProviderRegistry:
    """
    Registry of available language model
    providers.
    """

    def __init__(
        self,
    ) -> None:

        self._providers: dict[
            str,
            LanguageModel,
        ] = {}

    def register(
        self,
        name: str,
        provider: LanguageModel,
    ) -> None:

        self._providers[
            name
        ] = provider

    def get(
        self,
        name: str,
    ) -> LanguageModel:

        return self._providers[
            name
        ]

    def providers(
        self,
    ) -> tuple[LanguageModel, ...]:
        """
        Return all registered language
        model providers.
        """

        return tuple(
            self._providers.values()
        )