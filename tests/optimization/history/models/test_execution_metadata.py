from uuid import uuid4

from backend.optimization.history.models.execution_metadata import (
    ExecutionMetadata,
)


def test_execution_metadata():

    metadata = ExecutionMetadata(
        execution_id=uuid4(),
        trace_id=uuid4(),
        fingerprint="abc123",
        normalized_sql="SELECT * FROM users;",
        pipeline_name="optimization",
        pipeline_version="1.0",
        database="postgres",
        schema="public",
    )

    assert metadata.pipeline_name == "optimization"

    assert metadata.database == "postgres"

    assert metadata.executed_at is not None