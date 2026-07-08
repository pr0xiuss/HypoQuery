from __future__ import annotations

from uuid import UUID

from backend.optimization.history.models.execution_record import ExecutionRecord
from backend.optimization.history.repositories.execution_record_repository import ExecutionRecordRepository
from backend.optimization.history.search.search_criteria import SearchCriteria
from backend.optimization.history.search.search_result import SearchResult

class MemoryExecutionRecordRepository(
    ExecutionRecordRepository,
):
    """
    In-memory implementation of the
    history repository.
    """

    def __init__(
        self,
    ) -> None:

        self._records: dict[
            UUID,
            ExecutionRecord,
        ] = {}

    def save(
        self,
        record: ExecutionRecord,
    ) -> None:

        self._records[
            record.metadata.execution_id
        ] = record

    def find(
        self,
        execution_id: UUID,
    ) -> ExecutionRecord | None:

        return self._records.get(
            execution_id,
        )

    def list(
        self,
    ) -> tuple[
        ExecutionRecord,
        ...,
    ]:

        return tuple(
            self._records.values(),
        )

    def exists(
        self,
        execution_id: UUID,
    ) -> bool:

        return (
            execution_id
            in self._records
        )
    
    def search(
        self,
        criteria: SearchCriteria,
    ) -> SearchResult:
        """
        Searches execution records matching the supplied criteria.
        """

        result = SearchResult()

        for record in self._records.values():

            if (
                criteria.execution_id is not None
                and record.metadata.execution_id != criteria.execution_id
            ):
                continue

            if (
                criteria.fingerprint is not None
                and record.metadata.fingerprint != criteria.fingerprint
            ):
                continue

            if (
                criteria.database is not None
                and record.metadata.database != criteria.database
            ):
                continue

            if (
                criteria.schema is not None
                and record.metadata.schema != criteria.schema
            ):
                continue

            if (
                criteria.pipeline_name is not None
                and record.metadata.pipeline_name != criteria.pipeline_name
            ):
                continue

            if (
                criteria.minimum_improvement is not None
                and record.summary.estimated_improvement_percent
                < criteria.minimum_improvement
            ):
                continue

            if (
                criteria.maximum_improvement is not None
                and record.summary.estimated_improvement_percent
                > criteria.maximum_improvement
            ):
                continue

            if (
                criteria.executed_after is not None
                and record.metadata.executed_at
                < criteria.executed_after
            ):
                continue

            if (
                criteria.executed_before is not None
                and record.metadata.executed_at
                > criteria.executed_before
            ):
                continue

            result.add(
                record,
            )

        return result
    
    def delete(
        self,
        execution_id: UUID,
    ) -> None:

        self._records.pop(
            execution_id,
            None,
        )

    def count(
        self,
    ) -> int:

        return len(
            self._records,
        )