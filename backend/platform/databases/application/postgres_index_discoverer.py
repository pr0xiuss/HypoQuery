import psycopg
from uuid import uuid4, UUID
from backend.platform.databases.application.index_discoverer import (
    IndexDiscoverer,
)
from backend.platform.databases.domain.db_index import DatabaseIndex

class PostgresIndexDiscoverer(
    IndexDiscoverer,
):
    """
    PostgreSQL implementation of index discovery.
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
                n.nspname, t.relname, i.relname, am.amname, ix.indisunique, ix.indisprimary
                FROM pg_index ix JOIN pg_class i ON i.oid = ix.indexrelid 
                JOIN pg_class t ON t.oid = ix.indrelid
                JOIN pg_namespace n ON n.oid = t.relnamespace
                JOIN pg_am am ON am.oid = i.relam
                WHERE n.nspname NOT IN (
                    'pg_catalog',
                    'information_schema'
                )
                ORDER BY n.nspname, t.relname, i.relname;
                """
            )

            return [
                DatabaseIndex(
                    id=uuid4(),
                    connection_id=connection_id,
                    schema_name=row[0],
                    table_name=row[1],
                    name=row[2],
                    method=row[3],
                    unique=row[4],
                    primary=row[5],
                )
                for row in cursor.fetchall()
            ]