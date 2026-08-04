import psycopg
from uuid import uuid4, UUID
from backend.platform.databases.application.trigger_discoverer import (
    TriggerDiscoverer,
)
from backend.platform.databases.domain.db_trigger import DatabaseTrigger

class PostgresTriggerDiscoverer(
    TriggerDiscoverer,
):
    """
    PostgreSQL implementation of trigger discovery.
    """

    def discover(
        self,
        connection: psycopg.Connection,
        connection_id: UUID
    ) -> list[str]:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    event_object_schema,
                    event_object_table,
                    trigger_name,
                    event_manipulation,
                    action_timing
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
                DatabaseTrigger(
                    id=uuid4(),
                    connection_id=connection_id,
                    schema_name=row[0],
                    table_name=row[1],
                    name=row[2],
                    event=row[3],
                    timing=row[4],
                )
                for row in cursor.fetchall()
            ]