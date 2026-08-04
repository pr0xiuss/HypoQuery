import psycopg
from backend.platform.databases.domain.db_view import DatabaseView
from backend.platform.databases.application.view_discoverer import ViewDiscoverer
from uuid import uuid4, UUID

class PostgresViewDiscoverer(
    ViewDiscoverer,
):
    """
    PostgreSQL implementation of view discovery.
    """

    def discover(
        self,
        connection: psycopg.Connection,
        connection_id: UUID,
    ) -> list[DatabaseView]:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    table_schema,
                    table_name
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
                DatabaseView(
                    id=uuid4(),
                    connection_id=connection_id,
                    schema_name=row[0],
                    name=row[1],
                )
                for row in cursor.fetchall()
            ]