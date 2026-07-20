import psycopg

from backend.platform.databases.application.lock_statistics_discoverer import (
    LockStatisticsDiscoverer,
)


class PostgresLockStatisticsDiscoverer(
    LockStatisticsDiscoverer,
):
    """
    PostgreSQL implementation of lock statistics discovery.
    """

    def discover(
        self,
        connection: psycopg.Connection,
    ) -> dict[str, int]:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    COUNT(*) AS total_locks,
                    COUNT(*) FILTER (
                        WHERE granted
                    ) AS granted_locks,
                    COUNT(*) FILTER (
                        WHERE NOT granted
                    ) AS waiting_locks
                FROM pg_locks;
                """
            )

            result = cursor.fetchone()

            return {
                "total_locks": result[0],
                "granted_locks": result[1],
                "waiting_locks": result[2],
            }