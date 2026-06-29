from psycopg import Connection

from infrastructure.postgres.scripts.observability.models.optimization_run import (
    OptimizationRun,
)
from infrastructure.postgres.scripts.observability.repositories.base_repo import (
    BaseRepository,
)


class OptimizationRunRepository(BaseRepository):

    def __init__(self, connection: Connection):
        super().__init__(connection)

    def create(
        self,
        run: OptimizationRun,
    ) -> int:

        query = """
        INSERT INTO optimization_runs(
            trace_id,
            query_signature,
            query_type,
            classifier_route,
            pipeline_status,
            retry_count,
            original_cost,
            optimized_cost,
            cost_improvement_percent
        )
        VALUES (
            %s,%s,%s,%s,%s,%s,%s,%s,%s
        )
        RETURNING run_id
        """

        with self.connection.cursor() as cursor:

            cursor.execute(
                query,
                (
                    str(run.trace_id),
                    run.query_signature,
                    run.query_type.value,
                    run.classifier_route.value,
                    run.pipeline_status.value,
                    run.retry_count,
                    run.original_cost,
                    run.optimized_cost,
                    run.cost_improvement_percent,
                ),
            )

            return cursor.fetchone()[0]

    def mark_completed(
        self,
        run_id: int,
        optimized_cost: float,
        improvement: float,
    ):

        query = """
        UPDATE optimization_runs
        SET
            optimized_cost=%s,
            cost_improvement_percent=%s,
            pipeline_status='SUCCESS',
            completed_at=NOW()
        WHERE run_id=%s
        """

        with self.connection.cursor() as cursor:

            cursor.execute(
                query,
                (
                    optimized_cost,
                    improvement,
                    run_id,
                ),
            )

    def mark_failed(
        self,
        run_id: int,
    ):

        query = """
        UPDATE optimization_runs
        SET
            pipeline_status='FAILED',
            completed_at=NOW()
        WHERE run_id=%s
        """

        with self.connection.cursor() as cursor:

            cursor.execute(
                query,
                (run_id,),
            )
