from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from uuid import UUID

from backend.optimization.history.models.execution_record import ExecutionRecord
from backend.optimization.history.search.search_criteria import SearchCriteria
from backend.optimization.history.search.search_result import SearchResult

class ExecutionRecordRepository(
    ABC,
):
    """
    Repository abstraction for persisted
    execution records.
    """

    @abstractmethod
    def save(
        self,
        record: ExecutionRecord,
    ) -> None:
        """
        Persist an execution record.
        """

    @abstractmethod
    def find(
        self,
        execution_id: UUID,
    ) -> ExecutionRecord | None:
        """
        Finds an execution record by id.
        """

    @abstractmethod
    def list(
        self,
    ) -> tuple[
        ExecutionRecord,
        ...,
    ]:
        """
        Returns all execution records.
        """

    @abstractmethod
    def exists(
        self,
        execution_id: UUID,
    ) -> bool:
        """
        Checks whether an execution record exists.
        """

    @abstractmethod
    def delete(
        self,
        execution_id: UUID,
    ) -> None:
        """
        Deletes an execution record.
        """

    @abstractmethod
    def count(
        self,
    ) -> int:
        """
        Returns the total number of
        persisted execution records.
        """

    @abstractmethod
    def search(
        self,
        criteria: SearchCriteria,
    ) -> SearchResult:
        """
        Searches execution records matching
        the supplied criteria.
        """