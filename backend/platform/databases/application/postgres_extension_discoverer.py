import psycopg
from uuid import uuid4, UUID
from backend.platform.databases.application.extension_discoverer import (
    ExtensionDiscoverer,
)
from backend.platform.databases.domain.db_extension import DatabaseExtension

class PostgresExtensionDiscoverer(
    ExtensionDiscoverer,
):
    """
    PostgreSQL implementation of extension discovery.
    """

    def discover(
        self,
        connection: psycopg.Connection,
        connection_id: UUID,
    ) -> list[str]:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT extname,extversion
                FROM pg_extension
                ORDER BY extname;
                """
            )

            return [
                DatabaseExtension(
                    id=uuid4(),
                    connection_id=connection_id,
                    name=row[0],
                    version=row[1],
                )
                for row in cursor.fetchall()
            ]