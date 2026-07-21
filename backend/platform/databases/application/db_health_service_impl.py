from datetime import datetime, UTC
from time import perf_counter
from uuid import UUID

import psycopg

from backend.platform.databases.application.db_health_service import (
    DatabaseHealthService,
)
from backend.platform.databases.dto.db_health_result import (
    DatabaseHealthResult,
)
from backend.platform.databases.repositories.db_connection_repo import (
    DatabaseConnectionRepository,
)


class DatabaseHealthServiceImpl(
    DatabaseHealthService,
):
    def __init__(
        self,
        repository: DatabaseConnectionRepository,
    ):
        self._repository = repository

    def check_health(
        self,
        connection_id: UUID,
    ) -> DatabaseHealthResult:
        connection = self._repository.get_by_id(
            connection_id,
        )

        if connection is None:
            return DatabaseHealthResult(
                healthy=False,
                latency_ms=0,
                postgres_version=None,
                checked_at=datetime.now(UTC),
                error="Database connection not found.",
            )

        start = perf_counter()

        try:
            with psycopg.connect(
                host=connection.host,
                port=connection.port,
                dbname=connection.database_name,
                user=connection.username,
                password=connection.password,
            ) as db:
                with db.cursor() as cursor:
                    cursor.execute("SHOW server_version")

                    version = cursor.fetchone()[0]

            latency = (perf_counter() - start) * 1000

            return DatabaseHealthResult(
                healthy=True,
                latency_ms=latency,
                postgres_version=version,
                checked_at=datetime.now(UTC),
                error=None,
            )

        except psycopg.Error as ex:
            latency = (perf_counter() - start) * 1000

            return DatabaseHealthResult(
                healthy=False,
                latency_ms=latency,
                postgres_version=None,
                checked_at=datetime.now(UTC),
                error=str(ex),
            )