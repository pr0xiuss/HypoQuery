from backend.assistant.factories.provider_factory import (
    ProviderFactory,
)
from backend.assistant.providers.mock_provider import (
    MockProvider,
)
from backend.assistant.registry.provider_registry import (
    ProviderRegistry,
)


def test_provider_factory():

    registry = ProviderRegistry()

    provider = MockProvider()

    registry.register(
        "mock",
        provider,
    )

    factory = ProviderFactory(
        registry,
    )

    assert (
        factory.create(
            "mock",
        )
        is provider
    )