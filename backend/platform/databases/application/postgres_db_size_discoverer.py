import psycopg

from backend.platform.databases.application.db_size_discoverer import (
    DatabaseSizeDiscoverer,
)


class PostgresDatabaseSizeDiscoverer(
    DatabaseSizeDiscoverer,
):
    """
    PostgreSQL implementation of database size discovery.
    """

    def discover(
        self,
        connection: psycopg.Connection,
    ) -> int:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    pg_database_size(current_database());
                """
            )

            result = cursor.fetchone()

            return int(result[0])