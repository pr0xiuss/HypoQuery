from psycopg import Connection

from backend.ingestion.models.query_result import QueryResult
from backend.ingestion.query_catalog import QueryCatalog
from backend.ingestion.executor import QueryExecutor


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
