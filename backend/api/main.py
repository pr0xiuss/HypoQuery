from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.lifespan import lifespan
from backend.platform.config.settings import get_settings
from backend.api.middleware.logging_middleware import LoggingMiddleware
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)

register_routers(app)


app.add_middleware(LoggingMiddleware)