from __future__ import annotations

from backend.assistant.extensions.plugin import (
    Plugin,
)


class PluginRegistry:
    """
    Registry responsible for managing
    assistant platform plugins.
    """

    def __init__(
        self,
    ) -> None:

        self._plugins: dict[
            str,
            Plugin,
        ] = {}

    def register(
        self,
        plugin: Plugin,
    ) -> None:

        self._plugins[
            plugin.name
        ] = plugin

        plugin.register()

    def get(
        self,
        name: str,
    ) -> Plugin:

        return self._plugins[
            name
        ]

    def plugins(
        self,
    ) -> tuple[Plugin, ...]:

        return tuple(
            self._plugins.values()
        )