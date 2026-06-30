from __future__ import annotations

import os

from .settings import (
    DatabaseSettings,
    ObservabilitySettings,
    PipelineSettings,
    QueueSettings,
    Settings,
    WorkerSettings,
)


class SettingsFactory:
    """
    Creates application Settings from external configuration.

    Currently supports environment variables.
    """

    @staticmethod
    def create() -> Settings:

        database = DatabaseSettings(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "5432")),
            database=os.getenv("DB_NAME", "hypoquery"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "postgres"),
        )

        queue = QueueSettings(
            max_size=int(os.getenv("QUEUE_MAX_SIZE", "1000")),
            max_retries=int(os.getenv("QUEUE_MAX_RETRIES", "3")),
        )

        workers = WorkerSettings(
            worker_count=int(os.getenv("WORKER_COUNT", "2")),
        )

        pipeline = PipelineSettings(
            version=os.getenv("PIPELINE_VERSION", "1.0"),
        )

        observability = ObservabilitySettings(
            enabled=os.getenv(
                "OBSERVABILITY_ENABLED",
                "true",
            ).lower()
            == "true"
        )

        return Settings(
            database=database,
            queue=queue,
            workers=workers,
            pipeline=pipeline,
            observability=observability,
        )