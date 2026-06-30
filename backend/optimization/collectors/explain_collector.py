from psycopg import Connection
from backend.ingestion.models.query import Query

class ExplainCollector:

    def __init__(self, connection: Connection):
        self.connection = connection

    def collect(self, query: Query) -> dict:

        sql = query.sql

        explain_query = f"""
        EXPLAIN (
            ANALYZE,
            BUFFERS,
            VERBOSE,
            FORMAT JSON
        )
        {sql}
        """

        with self.connection.cursor() as cursor:

            cursor.execute(explain_query)

            result = cursor.fetchone()[0]

        # print(
        #     json.dumps(result[0], indent=4,)
        # )

        return result[0]
