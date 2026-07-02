from psycopg import Connection

from backend.ingestion.runner import WorkloadRunner


class Workload:

    def __init__(self, connection: Connection):

        self.runner = WorkloadRunner(connection)

    def execute(self):

        return self.runner.run()
