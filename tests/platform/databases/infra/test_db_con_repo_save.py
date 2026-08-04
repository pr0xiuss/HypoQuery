from uuid import uuid4
from datetime import datetime, UTC
from backend.platform.databases.domain.db_connection import DatabaseConnection
from backend.platform.databases.infra.db_connection_repo_impl import (
    DatabaseConnectionRepositoryImpl,
)


def test_save_persists_connection(
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

    result = repository.save(
        connection,
    )

    assert result.id == connection.id
    assert result.host == "localhost"
    assert result.database_name == "postgres"