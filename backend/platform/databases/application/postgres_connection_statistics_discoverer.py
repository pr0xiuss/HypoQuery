import psycopg

from backend.platform.databases.application.connection_statistics_discoverer import (
    ConnectionStatisticsDiscoverer,
)


class PostgresConnectionStatisticsDiscoverer(
    ConnectionStatisticsDiscoverer,
):
    """
    PostgreSQL implementation of connection statistics discovery.
    """

    def discover(
        self,
        connection: psycopg.Connection,
    ) -> dict[str, int]:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    COUNT(*) AS total_connections,
                    COUNT(*) FILTER (
                        WHERE state = 'active'
                    ) AS active_connections,
                    COUNT(*) FILTER (
                        WHERE state = 'idle'
                    ) AS idle_connections,
                    COUNT(*) FILTER (
                        WHERE wait_event IS NOT NULL
                    ) AS waiting_connections
                FROM pg_stat_activity
                WHERE datname = current_database();
                """
            )

            result = cursor.fetchone()

            return {
                "total_connections": result[0],
                "active_connections": result[1],
                "idle_connections": result[2],
                "waiting_connections": result[3],
            }