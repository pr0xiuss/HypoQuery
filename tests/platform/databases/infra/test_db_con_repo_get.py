from uuid import uuid4
from datetime import datetime, UTC
from backend.platform.databases.domain.db_connection import DatabaseConnection
from backend.platform.databases.infra.db_connection_repo_impl import (
    DatabaseConnectionRepositoryImpl,
)


def test_get_by_id_returns_connection(
    db_session,
    environment
) -> None:
    repository = DatabaseConnectionRepositoryImpl(
        db_session,
    )
    now = datetime.now(UTC)
    connection = DatabaseConnection(
        id=uuid4(),
        environment_id=environment.id,
        name="local",
        host="localhost",
        port=5432,
        database_name="postgres",
        username="postgres",
        password="password",
        ssl_enabled=False,
        is_active=True,
        created_at=now,
        updated_at=now,
    )

    repository.save(
        connection,
    )

    result = repository.get_by_id(
        connection.id,
    )

    assert result is not None
    assert result.id == connection.id