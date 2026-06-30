import time

from psycopg import Connection

from infrastructure.postgres.scripts.models.query import Query
from infrastructure.postgres.scripts.models.query_result import QueryResult


class QueryExecutor:

    def __init__(self, connection: Connection):
        self.connection = connection


    def execute(self, query: Query) -> QueryResult:

        start = time.perf_counter()

        try:
            with self.connection.cursor() as cursor:

                cursor.execute(query.sql)

                rows = cursor.fetchall() if cursor.description else []

            execution_time = (time.perf_counter() - start) * 1000

            return QueryResult(
                query_id=query.id,
                query_name=query.name,
                execution_time_ms=execution_time,
                rows_returned=len(rows),
                success=True,
                error=None,
            )

        except Exception as e:

            execution_time = (time.perf_counter() - start) * 1000

            self.connection.rollback()

            return QueryResult(
                query_id=query.id,
                query_name=query.name,
                execution_time_ms=execution_time,
                rows_returned=0,
                success=False,
                error=str(e),
            )
