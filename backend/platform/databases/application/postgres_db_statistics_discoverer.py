import psycopg

from backend.platform.databases.application.db_statistics_discoverer import (
    DatabaseStatisticsDiscoverer,
)


class PostgresDatabaseStatisticsDiscoverer(
    DatabaseStatisticsDiscoverer,
):
    """
    PostgreSQL implementation of database statistics discovery.
    """

    def discover(
        self,
        connection: psycopg.Connection,
    ) -> dict[str, int]:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    xact_commit,
                    xact_rollback,
                    blks_read,
                    blks_hit,
                    tup_returned,
                    tup_fetched,
                    tup_inserted,
                    tup_updated,
                    tup_deleted
                FROM pg_stat_database
                WHERE datname = current_database();
                """
            )

            result = cursor.fetchone()

            return {
                "transactions_committed": result[0],
                "transactions_rolled_back": result[1],
                "blocks_read": result[2],
                "blocks_hit": result[3],
                "tuples_returned": result[4],
                "tuples_fetched": result[5],
                "tuples_inserted": result[6],
                "tuples_updated": result[7],
                "tuples_deleted": result[8],
            }