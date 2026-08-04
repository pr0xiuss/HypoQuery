from fastapi import Request
from backend.platform.bootstrap.container import PlatformContainer



def get_container(request: Request) -> PlatformContainer:
    """
    Returns the application's dependency injection container.
    """
    return request.app.state.container