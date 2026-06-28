from psycopg import Connection
from psycopg.types.json import Jsonb
from infrastructure.postgres.scripts.observability.models.optimization_result import (
    OptimizationResult,
)
from infrastructure.postgres.scripts.observability.repositories.base_repo import (
    BaseRepository,
)


class OptimizationResultRepository(BaseRepository):

    def __init__(self, connection: Connection):
        super().__init__(connection)

    def save(
        self,
        result: OptimizationResult,
    ) -> None:

        query = """
        INSERT INTO optimization_results(
            run_id,
            diagnosis,
            remediation_type,
            recommended_index_sql,
            rewritten_query,
            llm_confidence,
            retrieval_score,
            faithfulness_score,
            validation_status,
            original_explain_plan,
            optimized_explain_plan
        )
        VALUES (
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
        )
        """

        with self.connection.cursor() as cursor:

            cursor.execute(
                query,
                (
                    result.run_id,
                    result.diagnosis,
                    result.remediation_type.value,
                    result.recommended_index_sql,
                    result.rewritten_query,
                    result.llm_confidence.value if result.llm_confidence else None,
                    result.retrieval_score,
                    result.faithfulness_score,
                    result.validation_status.value,
                    (
                        Jsonb(result.original_explain_plan)
                        if result.original_explain_plan is not None
                        else None
                    ),
                    (
                        Jsonb(result.optimized_explain_plan)
                        if result.optimized_explain_plan is not None
                        else None
                    ),
                ),
            )
