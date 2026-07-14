from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.platform.bootstrap.container import PlatformContainer


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    Manages the application lifecycle.

    Startup:
        - Initialize the dependency injection container.
        - Register platform resources.

    Shutdown:
        - Release platform resources gracefully.
    """

    container = PlatformContainer()

    app.state.container = container

    yield

    container.unwire()