from datetime import UTC, datetime
from uuid import uuid4

from backend.optimization.history.search.search_criteria import (
    SearchCriteria,
)


def test_search_criteria():

    now = datetime.now(
        UTC,
    )

    criteria = SearchCriteria(
        execution_id=uuid4(),
        fingerprint="abc123",
        database="postgres",
        schema="public",
        pipeline_name="optimization",
        minimum_improvement=40,
        maximum_improvement=90,
        executed_after=now,
        executed_before=now,
    )

    assert criteria.fingerprint == "abc123"

    assert criteria.database == "postgres"

    assert criteria.pipeline_name == "optimization"

    assert criteria.minimum_improvement == 40

    assert criteria.maximum_improvement == 90