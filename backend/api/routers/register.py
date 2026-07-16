from fastapi import FastAPI

from backend.api.routers.auth_router import (
    router as auth_router,
)
from backend.api.routers.environment_router import (
    router as environment_router,
)
from backend.api.routers.health_router import (
    router as health_router,
)
from backend.api.routers.org_router import (
    router as organization_router,
)
from backend.api.routers.project_router import (
    router as project_router,
)
from backend.api.routers.root_router import (
    router as root_router,
)
from backend.api.routers.system_router import (
    router as system_router,
)
from backend.api.routers.user_router import (
    router as user_router,
)


def register_routers(
    app: FastAPI,
) -> None:
    """
    Registers all API routers.
    """

    app.include_router(
        root_router,
        prefix="/api/v1",
        tags=["Root"],
    )

    app.include_router(
        system_router,
        prefix="/api/v1",
        tags=["System"],
    )

    app.include_router(
        health_router,
        prefix="/api/v1",
        tags=["Health"],
    )

    app.include_router(
        auth_router,
        prefix="/api/v1",
        tags=["Authentication"],
    )

    app.include_router(
        user_router,
        prefix="/api/v1",
        tags=["Users"],
    )

    app.include_router(
        organization_router,
        prefix="/api/v1",
        tags=["Organizations"],
    )

    app.include_router(
        project_router,
        prefix="/api/v1",
        tags=["Projects"],
    )

    app.include_router(
        environment_router,
        prefix="/api/v1",
        tags=["Environments"],
    )