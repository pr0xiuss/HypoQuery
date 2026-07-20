import psycopg

from backend.platform.databases.application.view_discoverer import (
    ViewDiscoverer,
)


class PostgresViewDiscoverer(
    ViewDiscoverer,
):
    """
    PostgreSQL implementation of view discovery.
    """

    def discover(
        self,
        connection: psycopg.Connection,
    ) -> list[str]:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    table_schema || '.' || table_name
                FROM information_schema.views
                WHERE table_schema NOT IN (
                    'pg_catalog',
                    'information_schema'
                )
                ORDER BY
                    table_schema,
                    table_name;
                """
            )

            return [
                row[0]
                for row in cursor.fetchall()
            ]