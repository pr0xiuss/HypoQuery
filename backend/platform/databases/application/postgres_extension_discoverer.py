import psycopg

from backend.platform.databases.application.extension_discoverer import (
    ExtensionDiscoverer,
)


class PostgresExtensionDiscoverer(
    ExtensionDiscoverer,
):
    """
    PostgreSQL implementation of extension discovery.
    """

    def discover(
        self,
        connection: psycopg.Connection,
    ) -> list[str]:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT extname
                FROM pg_extension
                ORDER BY extname;
                """
            )

            return [
                row[0]
                for row in cursor.fetchall()
            ]