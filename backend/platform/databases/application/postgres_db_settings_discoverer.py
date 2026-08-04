import psycopg

from backend.platform.databases.application.db_settings_discoverer import (
    DatabaseSettingsDiscoverer,
)


class PostgresDatabaseSettingsDiscoverer(
    DatabaseSettingsDiscoverer,
):
    """
    PostgreSQL implementation of database settings discovery.
    """

    def discover(
        self,
        connection: psycopg.Connection,
    ) -> dict[str, str]:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    name,
                    setting
                FROM pg_settings
                ORDER BY
                    name;
                """
            )

            return {
                row[0]: row[1]
                for row in cursor.fetchall()
            }