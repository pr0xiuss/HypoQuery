import psycopg

from backend.platform.databases.application.index_discoverer import (
    IndexDiscoverer,
)


class PostgresIndexDiscoverer(
    IndexDiscoverer,
):
    """
    PostgreSQL implementation of index discovery.
    """

    def discover(
        self,
        connection: psycopg.Connection,
    ) -> list[str]:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    schemaname || '.' || indexname
                FROM pg_indexes
                WHERE schemaname NOT IN (
                    'pg_catalog',
                    'information_schema'
                )
                ORDER BY
                    schemaname,
                    indexname;
                """
            )

            return [
                row[0]
                for row in cursor.fetchall()
            ]