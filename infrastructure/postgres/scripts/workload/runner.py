from psycopg import Connection

from infrastructure.postgres.scripts.models.query_result import QueryResult
from infrastructure.postgres.scripts.workload.query_catalog import QueryCatalog
from infrastructure.postgres.scripts.workload.executor import QueryExecutor


class WorkloadRunner:

    def __init__(self, connection: Connection):

        self.executor = QueryExecutor(connection)

    def run(self) -> list[QueryResult]:

        results = []

        queries = QueryCatalog.get_queries()

        for query in queries:

            result = self.executor.execute(query)

            results.append(result)

        return results