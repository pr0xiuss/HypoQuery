from unittest.mock import Mock
from uuid import uuid4

from backend.platform.databases.application.db_connection_service_impl import (
    DatabaseConnectionServiceImpl,
)


def test_delete_calls_repository() -> None:
    repository = Mock()

    service = DatabaseConnectionServiceImpl(
        repository=repository,
        validator=Mock(),
        discovery_service=Mock(),
        metadata_persistence_service=Mock(),
        health_service=Mock(),
    )

    connection_id = uuid4()

    service.delete(connection_id)

    repository.delete.assert_called_once_with(connection_id)