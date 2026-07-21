from unittest.mock import Mock
from uuid import uuid4

from backend.platform.databases.application.db_connection_service_impl import (
    DatabaseConnectionServiceImpl,
)


def test_get_returns_none_when_connection_missing() -> None:
    repository = Mock()

    repository.get_by_id.return_value = None

    service = DatabaseConnectionServiceImpl(
        repository=repository,
        validator=Mock(),
        discovery_service=Mock(),
        metadata_persistence_service=Mock(),
        health_service=Mock(),
    )

    result = service.get(
        uuid4(),
    )

    assert result is None