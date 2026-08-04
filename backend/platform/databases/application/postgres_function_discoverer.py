import psycopg
from uuid import uuid4, UUID
from backend.platform.databases.application.function_discoverer import (
    FunctionDiscoverer,
)
from backend.platform.databases.domain.db_function import DatabaseFunction


class PostgresFunctionDiscoverer(
    FunctionDiscoverer,
):
    """
    PostgreSQL implementation of function discovery.
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
                    routine_schema,
                    routine_name,
                    data_type
                FROM information_schema.routines
                WHERE routine_type = 'FUNCTION'
                AND routine_schema NOT IN (
                    'pg_catalog',
                    'information_schema'
                )
                ORDER BY
                    routine_schema,
                    routine_name;
                """
            )

            return [
                DatabaseFunction(
                    id=uuid4(),
                    connection_id=connection_id,
                    schema_name=row[0],
                    name=row[1],
                    return_type=row[2],
                )
                for row in cursor.fetchall()
            ]