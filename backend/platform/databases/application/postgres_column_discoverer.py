from uuid import UUID
from uuid import uuid4

import psycopg

from backend.platform.databases.application.column_discoverer import (
    ColumnDiscoverer,
)
from backend.platform.databases.domain.db_column import (
    DatabaseColumn,
)


class PostgresColumnDiscoverer(
    ColumnDiscoverer,
):
    """
    PostgreSQL implementation of column discovery.
    """

    def discover(
        self,
        connection: psycopg.Connection,
        connection_id: UUID,
    ) -> list[DatabaseColumn]:

        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT
                    table_schema,
                    table_name,
                    column_name,
                    data_type,
                    is_nullable,
                    column_default,
                    ordinal_position
                FROM information_schema.columns
                WHERE table_schema NOT IN (
                    'pg_catalog',
                    'information_schema'
                )
                ORDER BY
                    table_schema,
                    table_name,
                    ordinal_position;
                """
            )

            return [
                DatabaseColumn(
                    id=uuid4(),
                    connection_id=connection_id,
                    schema_name=row[0],
                    table_name=row[1],
                    name=row[2],
                    data_type=row[3],
                    nullable=row[4] == "YES",
                    default_value=row[5],
                    ordinal_position=row[6],
                )
                for row in cursor.fetchall()
            ]