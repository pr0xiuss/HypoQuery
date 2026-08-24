from typing import List
from psycopg import Connection

from backend.execution.observability.models.pipeline_log import (
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
                    log.log_level.value if hasattr(log.log_level, 'value') else log.log_level,
                    log.message,
                    log.duration_ms,
                    log.payload,
                ),
            )

    def list(
        self,
        limit: int = 100,
        offset: int = 0,
    ) -> List[PipelineLog]:
        query = """
            SELECT run_id, service_name, node_name, log_level, message, duration_ms, payload, created_at
            FROM pipeline_logs
            ORDER BY created_at DESC
            LIMIT %s OFFSET %s
        """
        with self.connection.cursor() as cursor:
            cursor.execute(query, (limit, offset))
            rows = cursor.fetchall()
            return [
                PipelineLog(
                    run_id=row[0],
                    service_name=row[1],
                    node_name=row[2],
                    log_level=row[3],
                    message=row[4],
                    duration_ms=row[5],
                    payload=row[6],
                    created_at=row[7],
                )
                for row in rows
            ]

    def get(
        self,
        run_id: int,
    ) -> List[PipelineLog]:
        query = """
            SELECT run_id, service_name, node_name, log_level, message, duration_ms, payload, created_at
            FROM pipeline_logs
            WHERE run_id = %s
            ORDER BY created_at DESC
        """
        with self.connection.cursor() as cursor:
            cursor.execute(query, (run_id,))
            rows = cursor.fetchall()
            return [
                PipelineLog(
                    run_id=row[0],
                    service_name=row[1],
                    node_name=row[2],
                    log_level=row[3],
                    message=row[4],
                    duration_ms=row[5],
                    payload=row[6],
                    created_at=row[7],
                )
                for row in rows
            ]
