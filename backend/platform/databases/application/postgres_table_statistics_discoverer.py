import psycopg

from backend.platform.databases.application.table_statistics_discoverer import (
    TableStatisticsDiscoverer,
)


class PostgresTableStatisticsDiscoverer(
    TableStatisticsDiscoverer,
):
    """
    PostgreSQL implementation of table statistics discovery.
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
                    seq_scan,
                    seq_tup_read,
                    idx_scan,
                    idx_tup_fetch,
                    n_tup_ins,
                    n_tup_upd,
                    n_tup_del,
                    n_live_tup,
                    n_dead_tup
                FROM pg_stat_user_tables
                ORDER BY
                    schemaname,
                    relname;
                """
            )

            return [
                {
                    "schema": row[0],
                    "table": row[1],
                    "sequential_scans": row[2],
                    "sequential_rows_read": row[3],
                    "index_scans": row[4],
                    "index_rows_fetched": row[5],
                    "rows_inserted": row[6],
                    "rows_updated": row[7],
                    "rows_deleted": row[8],
                    "live_rows": row[9],
                    "dead_rows": row[10],
                }
                for row in cursor.fetchall()
            ]