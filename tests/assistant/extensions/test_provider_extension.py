from backend.assistant.extensions.provider_extension import (
    ProviderExtension,
)
from backend.assistant.providers.mock_provider import (
    MockProvider,
)
from backend.assistant.registry.provider_registry import (
    ProviderRegistry,
)


def test_provider_extension():

    registry = ProviderRegistry()

    provider = MockProvider()

    extension = ProviderExtension(
        name="mock",
        provider=provider,
        registry=registry,
    )

    extension.register()

    assert (
        registry.get(
            "mock",
        )
        is provider
    )