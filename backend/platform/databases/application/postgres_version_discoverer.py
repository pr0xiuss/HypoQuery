import psycopg

from backend.platform.databases.application.version_discoverer import (
    VersionDiscoverer,
)


class PostgresVersionDiscoverer(
    VersionDiscoverer,
):
    """
    PostgreSQL implementation of version discovery.
    """

    def discover(
        self,
        connection: psycopg.Connection,
    ) -> str:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT version();",
            )

            return cursor.fetchone()[0]