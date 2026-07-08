from __future__ import annotations

from backend.optimization.history.repositories.execution_record_repository import (
    ExecutionRecordRepository,
)
from backend.optimization.history.search.search_criteria import (
    SearchCriteria,
)
from backend.optimization.history.search.search_result import (
    SearchResult,
)


class HistorySearchEngine:
    """
    Searches persisted execution history.
    """

    def __init__(
        self,
        repository: ExecutionRecordRepository,
    ) -> None:

        self._repository = repository

    def search(
        self,
        criteria: SearchCriteria,
    ) -> SearchResult:

        raise NotImplementedError