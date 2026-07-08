import pytest

from backend.optimization.history.repositories.memory_repository import (
    MemoryExecutionRecordRepository,
)
from backend.optimization.history.search.search_criteria import (
    SearchCriteria,
)
from backend.optimization.history.search.search_engine import (
    HistorySearchEngine,
)


def test_search_not_implemented():

    engine = HistorySearchEngine(
        MemoryExecutionRecordRepository(),
    )

    with pytest.raises(
        NotImplementedError,
    ):
        engine.search(
            SearchCriteria(),
        )