import psycopg
from uuid import uuid4, UUID
from backend.platform.databases.application.sequence_discoverer import (
    SequenceDiscoverer,
)
from backend.platform.databases.domain.db_sequence import DatabaseSequence

class PostgresSequenceDiscoverer(
    SequenceDiscoverer,
):
    """
    PostgreSQL implementation of sequence discovery.
    """

    def discover(
        self,
        connection: psycopg.Connection,
        connection_id: UUID,
    ) -> list[str]:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    sequence_schema,
                    sequence_name
                FROM information_schema.sequences
                WHERE sequence_schema NOT IN (
                    'pg_catalog',
                    'information_schema'
                )
                ORDER BY
                    sequence_schema,
                    sequence_name;
                """
            )

            return [
                DatabaseSequence(
                    id=uuid4(),
                    connection_id=connection_id,
                    schema_name=row[0],
                    name=row[1],
                )
                for row in cursor.fetchall()
            ]