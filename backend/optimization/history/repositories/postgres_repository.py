from __future__ import annotations

from uuid import UUID
import json
from psycopg import Connection
from dataclasses import asdict
from backend.optimization.history.models.execution_record import ExecutionRecord
from backend.optimization.history.repositories.execution_record_repository import ExecutionRecordRepository
from backend.optimization.history.search.search_criteria import SearchCriteria
from backend.optimization.history.search.search_result import SearchResult

class PostgresExecutionRecordRepository(
    ExecutionRecordRepository,
):
    """
    PostgreSQL-backed execution record repository.

    NOTE:
    This is currently a persistence skeleton.
    Full relational mapping will be implemented
    in the next iteration.
    """

    def __init__(
        self,
        connection: Connection,
    ) -> None:

        self._connection = connection

    def save(
        self,
        record: ExecutionRecord,
    ) -> None:

        summary = record.summary
        metadata = record.metadata

        snapshot = json.dumps(
            asdict(
                record.snapshot.report,
            ),
            default=str,
        )

        with self._connection.cursor() as cursor:

            cursor.execute(
                """
                INSERT INTO optimization_history
                (
                    execution_id,
                    trace_id,
                    fingerprint,
                    normalized_sql,
                    pipeline_name,
                    pipeline_version,
                    database_name,
                    schema_name,
                    executed_at,
                    recommendation_count,
                    validated_recommendation_count,
                    strategy_count,
                    estimated_improvement_percent,
                    highest_strategy_score,
                    snapshot_json
                )
                VALUES
                (
                    %s,%s,%s,%s,%s,%s,%s,%s,%s,
                    %s,%s,%s,%s,%s,%s
                )
                """,
                (
                    metadata.execution_id,
                    metadata.trace_id,
                    metadata.fingerprint,
                    metadata.normalized_sql,
                    metadata.pipeline_name,
                    metadata.pipeline_version,
                    metadata.database,
                    metadata.schema,
                    metadata.executed_at,
                    summary.total_recommendations,
                    summary.validated_recommendations,
                    summary.total_strategies,
                    summary.estimated_improvement_percent,
                    summary.highest_strategy_score,
                    snapshot,
                ),
            )

        self._connection.commit()

    def find(
        self,
        execution_id: UUID,
    ) -> ExecutionRecord | None:

        raise NotImplementedError

    def list(
        self,
    ) -> tuple[
        ExecutionRecord,
        ...,
    ]:

        raise NotImplementedError

    def exists(
        self,
        execution_id: UUID,
    ) -> bool:

        with self._connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT EXISTS
                (
                    SELECT 1
                    FROM optimization_history
                    WHERE execution_id = %s
                )
                """,
                (
                    execution_id,
                ),
            )

            return cursor.fetchone()[0]

    def delete(
        self,
        execution_id: UUID,
    ) -> None:

        with self._connection.cursor() as cursor:

            cursor.execute(
                """
                DELETE
                FROM optimization_history
                WHERE execution_id = %s
                """,
                (
                    execution_id,
                ),
            )

        self._connection.commit()

    def count(
        self,
    ) -> int:

        with self._connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM optimization_history
                """
            )

            return cursor.fetchone()[0]
        
    def search(
        self,
        criteria: SearchCriteria,
    ) -> SearchResult:

        raise NotImplementedError