from psycopg import Connection

from infrastructure.postgres.scripts.observability.models.pipeline_log import (
    PipelineLog,
)
from infrastructure.postgres.scripts.observability.repositories.base_repo import (
    BaseRepository,
)


class PipelineLogRepository(BaseRepository):

    def __init__(self, connection: Connection):
        super().__init__(connection)

    def save(
        self,
        log: PipelineLog,
    ) -> None:

        query = """
            INSERT INTO pipeline_logs(
                run_id,
                service_name,
                node_name,
                log_level,
                message,
                duration_ms,
                payload
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """

        with self.connection.cursor() as cursor:

            cursor.execute(
                query,
                (
                    log.run_id,
                    log.service_name,
                    log.node_name,
                    log.log_level.value,
                    log.message,
                    log.duration_ms,
                    log.payload,
                ),
            )