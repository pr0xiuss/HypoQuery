import pytest

from backend.assistant.registry.provider_registry import (
    ProviderRegistry,
)


def test_unknown_provider():

    registry = ProviderRegistry()

    with pytest.raises(
        KeyError,
    ):

        registry.get(
            "does_not_exist",
        )