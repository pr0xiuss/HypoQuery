from backend.assistant.health.provider_health import (
    ProviderHealth,
)
from backend.assistant.providers.mock_provider import (
    MockProvider,
)
from backend.assistant.registry.provider_registry import (
    ProviderRegistry,
)


def test_provider_health():

    registry = ProviderRegistry()

    registry.register(
        "mock",
        MockProvider(),
    )

    health = ProviderHealth(
        registry,
    )

    assert health.check()