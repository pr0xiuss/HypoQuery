from dependency_injector import containers
from dependency_injector import providers

from backend.platform.config.settings import Settings
from backend.platform.config.settings import get_settings


class PlatformContainer(containers.DeclarativeContainer):
    """
    Dependency Injection container for the Product Platform.

    This container owns only Phase 7 platform services.

    Engine services (Execution, Optimization, Knowledge,
    Operations, etc.) will be registered later through
    composition without modifying the engine.
    """

    wiring_config = containers.WiringConfiguration(
        packages=[
            "backend.api",
        ]
    )

    settings = providers.Singleton(
        get_settings,
    )