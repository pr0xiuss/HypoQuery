import psycopg

from backend.platform.databases.application.sequence_discoverer import (
    SequenceDiscoverer,
)


class PostgresSequenceDiscoverer(
    SequenceDiscoverer,
):
    """
    PostgreSQL implementation of sequence discovery.
    """

    def discover(
        self,
        connection: psycopg.Connection,
    ) -> list[str]:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    sequence_schema || '.' || sequence_name
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
                row[0]
                for row in cursor.fetchall()
            ]