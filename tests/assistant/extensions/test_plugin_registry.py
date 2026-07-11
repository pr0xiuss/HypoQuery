from backend.assistant.extensions.plugin import (
    Plugin,
)
from backend.assistant.extensions.plugin_registry import (
    PluginRegistry,
)


class FakePlugin(
    Plugin,
):

    def __init__(
        self,
    ) -> None:

        self._registered = False

    @property
    def name(
        self,
    ) -> str:

        return "fake"

    def register(
        self,
    ) -> None:

        self._registered = True


def test_plugin_registry():

    registry = PluginRegistry()

    plugin = FakePlugin()

    registry.register(
        plugin,
    )

    assert (
        registry.get(
            "fake",
        )
        is plugin
    )

    assert plugin._registered

    assert len(
        registry.plugins()
    ) == 1