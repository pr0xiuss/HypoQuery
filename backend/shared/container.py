from __future__ import annotations

from backend.shared.settings import Settings
from backend.shared.settings_factory import SettingsFactory


class Container:
    """
    Root dependency injection container.

    Responsible for creating and owning shared application
    dependencies.

    As the application grows, this container will expose
    factories for services, pipelines, queues, workers,
    collectors, APIs and infrastructure.
    """

    def __init__(
        self,
        settings: Settings | None = None,
    ) -> None:

        self._settings = settings or SettingsFactory.create()

    @property
    def settings(self) -> Settings:
        """
        Shared immutable application settings.
        """
        return self._settings