from fastapi import FastAPI

from backend.api.exception_handlers.global_exception_handler import unhandled_exception_handler
from backend.api.lifespan import lifespan
from backend.api.routers.root_router import router as root_router
from backend.api.routers.health_router import router as health_router
from backend.api.routers.system_router import router as system_router
from backend.platform.config.settings import get_settings
from backend.api.middleware.logging_middleware import LoggingMiddleware


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="Enterprise PostgreSQL Workload Intelligence Platform",
    version=settings.app_version,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.add_exception_handler(
    Exception,
    unhandled_exception_handler,
)

app.include_router(
    root_router,
    prefix="/api/v1",
    tags=["Root"],
)

app.include_router(
    health_router,
    prefix="/api/v1",
    tags=["Health"],
)

app.include_router(
    system_router,
    prefix="/api/v1",
    tags=["System"],
)

app.add_middleware(LoggingMiddleware)