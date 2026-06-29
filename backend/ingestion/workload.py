from psycopg import Connection

from infrastructure.postgres.scripts.workload.runner import WorkloadRunner


class Workload:

    def __init__(self, connection: Connection):

        self.runner = WorkloadRunner(connection)

    def execute(self):

        return self.runner.run()
