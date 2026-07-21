from uuid import uuid4
from datetime import datetime, UTC
from backend.platform.databases.domain.db_connection import DatabaseConnection
from backend.platform.databases.infra.db_connection_repo_impl import (
    DatabaseConnectionRepositoryImpl,
)


def test_list_by_environment_returns_connections(
    db_session,
    environment
) -> None:
    repository = DatabaseConnectionRepositoryImpl(
        db_session,
    )
    now = datetime.now(UTC)
    environment_id = environment.id

    for name in ("db1", "db2"):
        repository.save(
            DatabaseConnection(
                id=uuid4(),
                environment_id=environment.id,
                name=name,
                host="localhost",
                port=5432,
                database_name=name,
                username="postgres",
                password="password",
                ssl_enabled=False,
                is_active=True,
                created_at=now,
                updated_at=now,
            )
        )

    result = repository.list_by_environment(
        environment_id,
    )

    assert len(result) == 2