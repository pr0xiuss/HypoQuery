from __future__ import annotations

from dataclasses import dataclass, field

@dataclass(frozen=True)
class SeedConfig:
    customers: int = 1000
    products: int = 5000
    orders: int = 20000
    reviews: int = 10000
    inventory: int = 5000
    product_events: int = 50000


CONFIG = SeedConfig()

@dataclass(frozen=True, slots=True)
class DatabaseSettings:
    """
    Database configuration.
    """

    host: str = "localhost"
    port: int = 5432
    database: str = "hypoquery"
    user: str = "postgres"
    password: str = "postgres"


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