import psycopg

from backend.platform.databases.application.table_discoverer import (
    TableDiscoverer,
)


class PostgresTableDiscoverer(
    TableDiscoverer,
):
    """
    PostgreSQL implementation of table discovery.
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
                FROM information_schema.tables
                WHERE table_type = 'BASE TABLE'
                  AND table_schema NOT IN (
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