import psycopg

from backend.platform.databases.application.index_statistics_discoverer import (
    IndexStatisticsDiscoverer,
)


class PostgresIndexStatisticsDiscoverer(
    IndexStatisticsDiscoverer,
):
    """
    PostgreSQL implementation of index statistics discovery.
    """

    def discover(
        self,
        connection: psycopg.Connection,
    ) -> list[dict[str, int | str]]:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    schemaname,
                    relname,
                    indexrelname,
                    idx_scan,
                    idx_tup_read,
                    idx_tup_fetch
                FROM pg_stat_user_indexes
                ORDER BY
                    schemaname,
                    relname,
                    indexrelname;
                """
            )

            return [
                {
                    "schema": row[0],
                    "table": row[1],
                    "index": row[2],
                    "index_scans": row[3],
                    "index_tuples_read": row[4],
                    "index_tuples_fetched": row[5],
                }
                for row in cursor.fetchall()
            ]