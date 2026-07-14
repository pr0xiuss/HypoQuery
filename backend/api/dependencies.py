from fastapi import Request

from backend.platform.bootstrap.container import PlatformContainer
from backend.platform.config.settings import Settings


def get_container(request: Request) -> PlatformContainer:
    """
    Returns the application's dependency injection container.
    """
    return request.app.state.container


def get_application_settings(request: Request) -> Settings:
    """
    FastAPI dependency that provides application settings through
    the dependency injection container.
    """
    container = get_container(request)

    return container.settings()