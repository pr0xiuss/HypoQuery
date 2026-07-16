from fastapi import FastAPI
from backend.api.exception_handlers.global_exception_handler import unhandled_exception_handler
from backend.api.lifespan import lifespan
from backend.api.routers.root_router import router as root_router
from backend.api.routers.health_router import router as health_router
from backend.api.routers.system_router import router as system_router
from backend.platform.config.settings import get_settings
from backend.api.middleware.logging_middleware import LoggingMiddleware
from backend.api.routers.auth_router import router as auth_router
from backend.api.routers.health_router import router as health_router
from backend.api.routers.org_router import router as organization_router
from backend.api.routers.root_router import router as root_router
from backend.api.routers.system_router import router as system_router
from backend.api.routers.environment_router import router as environment_router
from backend.api.routers.project_router import router as project_router
from backend.api.routers.user_router import router as user_router
from backend.api.exception_handlers.register import register_exception_handlers
from backend.api.routers.register import register_routers

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

register_exception_handlers(app)

register_routers(app)


app.add_middleware(LoggingMiddleware)