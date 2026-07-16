from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from fastapi import FastAPI
from backend.platform.bootstrap.container import PlatformContainer
from backend.platform.shared.database import verify_database_connection


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    Manages the application lifecycle.

    Startup:
        - Verify platform database connectivity.
        - Initialize the dependency injection container.
        - Register platform resources.

    Shutdown:
        - Release platform resources gracefully.
    """

    verify_database_connection()

    container = PlatformContainer()

    app.state.container = container

    yield

    container.unwire()