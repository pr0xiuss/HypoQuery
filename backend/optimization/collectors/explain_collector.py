from __future__ import annotations

from psycopg import Connection

from backend.ingestion.models.query import Query


class ExplainCollector:
    """
    Executes EXPLAIN ANALYZE and returns the PostgreSQL JSON plan.
    """

    def __init__(self, connection: Connection,) -> None:

        self._connection = connection

    def collect(self, query: Query | str,) -> dict:

        sql = (
            query.sql
            if isinstance(query, Query)
            else query
        )

        explain_query = f"""
        EXPLAIN (
            ANALYZE,
            BUFFERS,
            VERBOSE,
            FORMAT JSON
        )
        {sql}
        """

        with self._connection.cursor() as cursor:

            cursor.execute(
                explain_query,
            )

            result = cursor.fetchone()[0]

        return result[0]