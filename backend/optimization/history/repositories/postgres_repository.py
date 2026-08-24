from __future__ import annotations

from uuid import UUID
import json
from psycopg import Connection
from psycopg.rows import tuple_row
from pydantic import TypeAdapter

from backend.optimization.history.models.execution_record import ExecutionRecord
from backend.optimization.history.models.execution_metadata import ExecutionMetadata
from backend.optimization.history.models.execution_summary import ExecutionSummary
from backend.optimization.history.models.optimization_snapshot import OptimizationSnapshot
from backend.optimization.history.repositories.execution_record_repository import ExecutionRecordRepository
from backend.optimization.history.search.search_criteria import SearchCriteria
from backend.optimization.history.search.search_result import SearchResult


class PostgresExecutionRecordRepository(
    ExecutionRecordRepository,
):
    """
    PostgreSQL-backed execution record repository.
    """

    def __init__(
        self,
        connection: Connection,
    ) -> None:

        self._connection = connection
        self._snapshot_adapter = TypeAdapter(OptimizationSnapshot)

    def save(
        self,
        record: ExecutionRecord,
    ) -> None:

        summary = record.summary
        metadata = record.metadata

        snapshot = self._snapshot_adapter.dump_json(
            record.snapshot,
        ).decode("utf-8")

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
                ON CONFLICT (execution_id) DO UPDATE SET
                    trace_id = EXCLUDED.trace_id,
                    fingerprint = EXCLUDED.fingerprint,
                    normalized_sql = EXCLUDED.normalized_sql,
                    pipeline_name = EXCLUDED.pipeline_name,
                    pipeline_version = EXCLUDED.pipeline_version,
                    database_name = EXCLUDED.database_name,
                    schema_name = EXCLUDED.schema_name,
                    executed_at = EXCLUDED.executed_at,
                    recommendation_count = EXCLUDED.recommendation_count,
                    validated_recommendation_count = EXCLUDED.validated_recommendation_count,
                    strategy_count = EXCLUDED.strategy_count,
                    estimated_improvement_percent = EXCLUDED.estimated_improvement_percent,
                    highest_strategy_score = EXCLUDED.highest_strategy_score,
                    snapshot_json = EXCLUDED.snapshot_json
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

    def _row_to_record(self, row: tuple) -> ExecutionRecord:
        (
            execution_id, trace_id, fingerprint, normalized_sql,
            pipeline_name, pipeline_version, database_name, schema_name,
            executed_at, recommendation_count, validated_recommendation_count,
            strategy_count, estimated_improvement_percent, highest_strategy_score,
            snapshot_json
        ) = row

        metadata = ExecutionMetadata(
            execution_id=execution_id,
            trace_id=trace_id,
            fingerprint=fingerprint,
            normalized_sql=normalized_sql,
            pipeline_name=pipeline_name,
            pipeline_version=pipeline_version,
            database=database_name,
            schema=schema_name,
            executed_at=executed_at,
        )

        summary = ExecutionSummary(
            total_recommendations=recommendation_count,
            validated_recommendations=validated_recommendation_count,
            total_strategies=strategy_count,
            estimated_improvement_percent=estimated_improvement_percent,
            highest_strategy_score=highest_strategy_score,
        )

        snapshot_dict = snapshot_json if isinstance(snapshot_json, dict) else json.loads(snapshot_json)
        snapshot = self._snapshot_adapter.validate_python(snapshot_dict)

        return ExecutionRecord(
            metadata=metadata,
            summary=summary,
            snapshot=snapshot,
        )

    def find(
        self,
        execution_id: UUID,
    ) -> ExecutionRecord | None:

        with self._connection.cursor(row_factory=tuple_row) as cursor:
            cursor.execute(
                """
                SELECT 
                    execution_id, trace_id, fingerprint, normalized_sql,
                    pipeline_name, pipeline_version, database_name, schema_name,
                    executed_at, recommendation_count, validated_recommendation_count,
                    strategy_count, estimated_improvement_percent, highest_strategy_score,
                    snapshot_json
                FROM optimization_history
                WHERE execution_id = %s
                """,
                (execution_id,)
            )
            row = cursor.fetchone()
            if not row:
                return None
            return self._row_to_record(row)

    def list(
        self,
    ) -> tuple[ExecutionRecord, ...]:

        with self._connection.cursor(row_factory=tuple_row) as cursor:
            cursor.execute(
                """
                SELECT 
                    execution_id, trace_id, fingerprint, normalized_sql,
                    pipeline_name, pipeline_version, database_name, schema_name,
                    executed_at, recommendation_count, validated_recommendation_count,
                    strategy_count, estimated_improvement_percent, highest_strategy_score,
                    snapshot_json
                FROM optimization_history
                ORDER BY executed_at DESC
                """
            )
            rows = cursor.fetchall()
            return tuple(self._row_to_record(row) for row in rows)

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
                (execution_id,),
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
                (execution_id,),
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

        result = SearchResult()
        query_parts = []
        params = []

        if criteria.execution_id is not None:
            query_parts.append("execution_id = %s")
            params.append(criteria.execution_id)
        if criteria.fingerprint is not None:
            query_parts.append("fingerprint = %s")
            params.append(criteria.fingerprint)
        if criteria.database is not None:
            query_parts.append("database_name = %s")
            params.append(criteria.database)
        if criteria.schema is not None:
            query_parts.append("schema_name = %s")
            params.append(criteria.schema)
        if criteria.pipeline_name is not None:
            query_parts.append("pipeline_name = %s")
            params.append(criteria.pipeline_name)
        if criteria.minimum_improvement is not None:
            query_parts.append("estimated_improvement_percent >= %s")
            params.append(criteria.minimum_improvement)
        if criteria.maximum_improvement is not None:
            query_parts.append("estimated_improvement_percent <= %s")
            params.append(criteria.maximum_improvement)
        if criteria.executed_after is not None:
            query_parts.append("executed_at >= %s")
            params.append(criteria.executed_after)
        if criteria.executed_before is not None:
            query_parts.append("executed_at <= %s")
            params.append(criteria.executed_before)

        where_clause = ""
        if query_parts:
            where_clause = "WHERE " + " AND ".join(query_parts)

        query = f"""
            SELECT 
                execution_id, trace_id, fingerprint, normalized_sql,
                pipeline_name, pipeline_version, database_name, schema_name,
                executed_at, recommendation_count, validated_recommendation_count,
                strategy_count, estimated_improvement_percent, highest_strategy_score,
                snapshot_json
            FROM optimization_history
            {where_clause}
            ORDER BY executed_at DESC
        """

        with self._connection.cursor(row_factory=tuple_row) as cursor:
            cursor.execute(query, tuple(params))
            rows = cursor.fetchall()
            for row in rows:
                result.add(self._row_to_record(row))

        return result