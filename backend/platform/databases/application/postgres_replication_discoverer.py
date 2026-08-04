import psycopg

from backend.platform.databases.application.replication_discoverer import (
    ReplicationDiscoverer,
)


class PostgresReplicationDiscoverer(
    ReplicationDiscoverer,
):
    """
    PostgreSQL implementation of replication discovery.
    """

    def discover(
        self,
        connection: psycopg.Connection,
    ) -> dict[str, int | bool]:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    pg_is_in_recovery(),
                    (
                        SELECT COUNT(*)
                        FROM pg_stat_replication
                    );
                """
            )

            is_replica, replica_count = cursor.fetchone()

            return {
                "is_replica": is_replica,
                "connected_replicas": replica_count,
            }