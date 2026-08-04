from fastapi import Request
from backend.platform.config.settings import Settings
from backend.api.dependencies.container import get_container


def get_application_settings(request: Request) -> Settings:
    """
    FastAPI dependency that provides application settings through
    the dependency injection container.
    """
    container = get_container(request)

    return container.settings()