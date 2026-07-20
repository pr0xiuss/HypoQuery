import psycopg

from backend.platform.databases.application.function_discoverer import (
    FunctionDiscoverer,
)


class PostgresFunctionDiscoverer(
    FunctionDiscoverer,
):
    """
    PostgreSQL implementation of function discovery.
    """

    def discover(
        self,
        connection: psycopg.Connection,
    ) -> list[str]:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    routine_schema || '.' || routine_name
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
                row[0]
                for row in cursor.fetchall()
            ]