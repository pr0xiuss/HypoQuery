from unittest.mock import Mock
from uuid import uuid4

from backend.platform.databases.application.db_connection_service_impl import (
    DatabaseConnectionServiceImpl,
)


def test_refresh_metadata_discovers_and_persists_metadata() -> None:
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

    discovery_result = Mock()

    discovery.discover.return_value = discovery_result

    service.refresh_metadata(
        connection_id,
    )

    discovery.discover.assert_called_once_with(
        connection_id,
    )

    persistence.refresh.assert_called_once_with(
        connection_id,
        discovery_result,
    )