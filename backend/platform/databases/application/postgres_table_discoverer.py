from uuid import uuid4, UUID
import psycopg
from backend.platform.databases.application.table_discoverer import TableDiscoverer
from backend.platform.databases.domain.db_table import DatabaseTable


class PostgresTableDiscoverer(
    TableDiscoverer,
):
    """
    PostgreSQL implementation of table discovery.
    """

    def discover(
        self,
        connection: psycopg.Connection,
        connection_id: UUID
    ) -> list[DatabaseTable]:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    n.nspname,
                    c.relname,
                    CASE
                        WHEN c.reltuples < 0 THEN NULL
                        ELSE c.reltuples::bigint
                    END,
                    pg_total_relation_size(c.oid),
                    (
                        SELECT COUNT(*)
                        FROM information_schema.columns cols
                        WHERE cols.table_schema = n.nspname
                        AND cols.table_name = c.relname
                    ),
                    EXISTS (
                        SELECT 1
                        FROM pg_constraint con
                        WHERE con.conrelid = c.oid
                        AND con.contype = 'p'
                    )
                FROM pg_class c
                JOIN pg_namespace n
                    ON n.oid = c.relnamespace
                WHERE c.relkind = 'r'
                AND n.nspname NOT IN (
                    'pg_catalog',
                    'information_schema'
                )
                ORDER BY
                    n.nspname,
                    c.relname;
                """
            )

            return [
                DatabaseTable(
                    id=uuid4(),
                    connection_id=connection_id,
                    schema_name=row[0],
                    name=row[1],
                    estimated_rows=row[2],
                    size_bytes=row[3],
                    column_count=row[4],
                    has_primary_key=row[5],
                )
                for row in cursor.fetchall()
            ]