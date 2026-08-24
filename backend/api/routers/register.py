from fastapi import FastAPI

from backend.api.routers.auth_router import router as auth_router
from backend.api.routers.environment_router import router as environment_router
from backend.api.routers.health_router import router as health_router
from backend.api.routers.org_router import router as organization_router
from backend.api.routers.project_router import router as project_router
from backend.api.routers.root_router import router as root_router
from backend.api.routers.system_router import router as system_router
from backend.api.routers.user_router import router as user_router
from backend.platform.databases.api.db_connection_router import router as database_connection_router
from backend.platform.apis.api.api_router import router as api_router


from backend.assistant.api.assistant_router import router as assistant_router
from backend.knowledge.api.knowledge_router import router as knowledge_router
from backend.product.dashboard.dashboard_router import router as dashboard_router
from backend.product.workloads.workload_router import router as workload_router
from backend.product.queries.query_router import router as query_router
from backend.product.operations.operations_router import router as operations_router
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
    
    app.include_router(
        database_connection_router,
        prefix="/api/v1",
        tags=["Database Connections"],
    )

    app.include_router(
        api_router,
        prefix="/api/v1",
        tags=["APIs"],
    )
    app.include_router(
        assistant_router,
        prefix="/api/v1",
    )
    app.include_router(
        knowledge_router,
        prefix="/api/v1",
    )
    app.include_router(
        dashboard_router,
        prefix="/api/v1",
    )
    app.include_router(
        workload_router,
        prefix="/api/v1",
    )
    app.include_router(
        query_router,
        prefix="/api/v1",
    )
    app.include_router(
        operations_router,
        prefix="/api/v1",
    )
