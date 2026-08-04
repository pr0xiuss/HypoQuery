from unittest.mock import Mock
from uuid import uuid4

from backend.platform.databases.application.db_connection_service_impl import (
    DatabaseConnectionServiceImpl,
)
from backend.platform.databases.domain.db_connection import DatabaseConnection
from backend.platform.databases.dto.create_db_connection_request import (
    CreateDatabaseConnectionRequest,
)


def test_create_saves_connection_and_refreshes_metadata() -> None:
    repository = Mock()
    validator = Mock()
    discovery = Mock()
    persistence = Mock()
    health = Mock()

    service = DatabaseConnectionServiceImpl(
        repository=repository,
        validator=validator,
        discovery_service=discovery,
        metadata_persistence_service=persistence,
        health_service=health,
    )

    environment_id = uuid4()

    request = CreateDatabaseConnectionRequest(
        name="local",
        host="localhost",
        port=5432,
        database_name="postgres",
        username="postgres",
        password="password",
        ssl_enabled=False,
    )

    saved = Mock(spec=DatabaseConnection)
    saved.id = uuid4()

    repository.save.return_value = saved

    result = service.create(
        environment_id,
        request,
    )

    validator.validate.assert_called_once_with(request)
    repository.save.assert_called_once()
    discovery.discover.assert_called_once_with(saved.id)
    persistence.refresh.assert_called_once()
    assert result == saved