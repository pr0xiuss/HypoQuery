import json

from psycopg import Connection


class ExplainCollector:

    def __init__(self, connection: Connection):
        self.connection = connection

    def collect(self, sql: str) -> dict:

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

        print(
            json.dumps(result[0], indent=4,)
        )

        return result[0]