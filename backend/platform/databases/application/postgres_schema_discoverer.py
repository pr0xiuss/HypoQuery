import psycopg

from backend.platform.databases.application.schema_discoverer import (
    SchemaDiscoverer,
)


class PostgresSchemaDiscoverer(
    SchemaDiscoverer,
):
    """
    PostgreSQL implementation of schema discovery.
    """

    def discover(
        self,
        connection: psycopg.Connection,
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
                row[0]
                for row in cursor.fetchall()
            ]