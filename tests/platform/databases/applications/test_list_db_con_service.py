from datetime import UTC, datetime
from unittest.mock import Mock
from uuid import uuid4

from backend.platform.databases.application.db_connection_service_impl import (
    DatabaseConnectionServiceImpl,
)
from backend.platform.databases.domain.db_connection import DatabaseConnection


def test_list_returns_all_connections() -> None:
    repository = Mock()

    service = DatabaseConnectionServiceImpl(
        repository=repository,
        validator=Mock(),
        discovery_service=Mock(),
        metadata_persistence_service=Mock(),
        health_service=Mock(),
    )

    connection = Mock(spec=DatabaseConnection)

    connection.id = uuid4()
    connection.environment_id = uuid4()
    connection.name = "local"
    connection.host = "localhost"
    connection.port = 5432
    connection.database_name = "postgres"
    connection.username = "postgres"
    connection.ssl_enabled = False
    connection.is_active = True
    connection.created_at = datetime.now(UTC)
    connection.updated_at = datetime.now(UTC)

    repository.list_by_environment.return_value = [connection]

    result = service.list(connection.environment_id)

    assert len(result) == 1
    assert result[0].id == connection.id
    repository.list_by_environment.assert_called_once_with(
        connection.environment_id,
    )