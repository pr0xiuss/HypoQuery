from unittest.mock import Mock
from uuid import uuid4

from backend.platform.databases.application.db_connection_service_impl import (
    DatabaseConnectionServiceImpl,
)


def test_check_health_delegates_to_health_service() -> None:
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

    connection_id = uuid4()

    expected = Mock()

    health.check_health.return_value = expected

    result = service.check_health(
        connection_id,
    )

    health.check_health.assert_called_once_with(
        connection_id,
    )

    assert result == expected