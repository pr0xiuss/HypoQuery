from backend.optimization.history.repositories.postgres_repository import (
    PostgresExecutionRecordRepository,
)


def test_repository_creation(
    db_connection,
):

    repository = (
        PostgresExecutionRecordRepository(
            db_connection,
        )
    )

    assert repository is not None