import psycopg
from backend.platform.databases.domain.db_schema import DatabaseSchema
from backend.platform.databases.application.schema_discoverer import (
    SchemaDiscoverer,
)
from uuid import uuid4, UUID

class PostgresSchemaDiscoverer(
    SchemaDiscoverer,
):
    """
    PostgreSQL implementation of schema discovery.
    """

    def discover(
        self,
        connection: psycopg.Connection,
        connection_id: UUID,
    ) -> list[str]:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT schema_name
                FROM information_schema.schemata
                WHERE schema_name NOT IN (
                    'pg_catalog',
                    'information_schema'
                )
                ORDER BY schema_name;
                """
            )

            return [
                DatabaseSchema(
                    id=uuid4(),
                    connection_id=connection_id,
                    name=row[0],
                )
                for row in cursor.fetchall()
            ]