from __future__ import annotations

from backend.assistant.health.health_check import (
    HealthCheck,
)
from backend.assistant.registry.provider_registry import (
    ProviderRegistry,
)


class ProviderHealth(
    HealthCheck,
):
    """
    Verifies that at least one language
    model provider is registered.
    """

    def __init__(
        self,
        registry: ProviderRegistry,
    ) -> None:

        self._registry = registry

    @property
    def name(
        self,
    ) -> str:

        return "provider"

    def check(
        self,
    ) -> bool:

        return (
            len(
                self._registry.providers()
            )
            > 0
        )