import psycopg

from backend.platform.databases.application.trigger_discoverer import (
    TriggerDiscoverer,
)


class PostgresTriggerDiscoverer(
    TriggerDiscoverer,
):
    """
    PostgreSQL implementation of trigger discovery.
    """

    def discover(
        self,
        connection: psycopg.Connection,
    ) -> list[str]:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    event_object_schema || '.' || trigger_name
                FROM information_schema.triggers
                WHERE trigger_schema NOT IN (
                    'pg_catalog',
                    'information_schema'
                )
                ORDER BY
                    event_object_schema,
                    trigger_name;
                """
            )

            return [
                row[0]
                for row in cursor.fetchall()
            ]