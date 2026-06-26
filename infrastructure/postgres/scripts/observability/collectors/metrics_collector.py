from psycopg import Connection


class MetricsCollector:

    def __init__(
        self,
        connection: Connection,
    ):
        self.connection = connection

    def collect(self):

        pass