from __future__ import annotations
from dataclasses import dataclass, field
import os
from dotenv import load_dotenv


load_dotenv()
@dataclass(frozen=True)
class SeedConfig:
    customers: int = 1000
    products: int = 5000
    orders: int = 20000
    reviews: int = 10000
    inventory: int = 5000
    product_events: int = 50000


CONFIG = SeedConfig()

def _require_env(
    name: str,
) -> str:

    value = os.getenv(
        name,
    )

    if not value:
        raise RuntimeError(
            f"Missing required environment variable: {name}",
        )

    return value

@dataclass(frozen=True, slots=True)
class DatabaseSettings:
    """
    Database configuration.
    """

    host: str = field(
        default_factory=lambda: _require_env(
            "POSTGRES_HOST",
        )
    )

    port: int = field(
        default_factory=lambda: int(
            _require_env(
                "POSTGRES_PORT",
            )
        )
    )

    database: str = field(
        default_factory=lambda: _require_env(
            "POSTGRES_DB",
        )
    )

    user: str = field(
        default_factory=lambda: _require_env(
            "POSTGRES_USER",
        )
    )

    password: str = field(
        default_factory=lambda: _require_env(
            "POSTGRES_PASSWORD",
        )
    )

@dataclass(frozen=True, slots=True)
class AssistantSettings:
    """
    Gemini configuration.
    """

    api_key: str = field(
        default_factory=lambda: _require_env(
            "GEMINI_API_KEY",
        )
    )

    model: str = field(
        default_factory=lambda: _require_env(
            "GEMINI_MODEL",
        )
    )

    temperature: float = field(
        default_factory=lambda: float(
            _require_env(
                "GEMINI_TEMPERATURE",
            )
        )
    )

    max_tokens: int = field(
        default_factory=lambda: int(
            _require_env(
                "GEMINI_MAX_TOKENS",
            )
        )
    )


@dataclass(frozen=True, slots=True)
class QueueSettings:
    """
    Queue configuration.
    """

    max_size: int = 1000
    max_retries: int = 3


@dataclass(frozen=True, slots=True)
class WorkerSettings:
    """
    Worker configuration.
    """

    worker_count: int = 2


@dataclass(frozen=True, slots=True)
class PipelineSettings:
    """
    Pipeline execution configuration.
    """

    version: str = "1.0"


@dataclass(frozen=True, slots=True)
class ObservabilitySettings:
    """
    Observability configuration.
    """

    enabled: bool = True


@dataclass(frozen=True, slots=True)
class Settings:
    """
    Root application settings.

    Acts as the single configuration object
    shared across the application.
    """

    database: DatabaseSettings = field(
        default_factory=DatabaseSettings
    )

    assistant: AssistantSettings = field(
        default_factory=AssistantSettings,
    )

    queue: QueueSettings = field(
        default_factory=QueueSettings
    )

    workers: WorkerSettings = field(
        default_factory=WorkerSettings
    )

    pipeline: PipelineSettings = field(
        default_factory=PipelineSettings
    )

    observability: ObservabilitySettings = field(
        default_factory=ObservabilitySettings
    )

settings = Settings()