from unittest.mock import Mock
from uuid import uuid4

from backend.platform.databases.application.db_health_service_impl import (
    DatabaseHealthServiceImpl,
)


def test_repository_is_called_once() -> None:
    repository = Mock()

    repository.get_by_id.return_value = None

    service = DatabaseHealthServiceImpl(
        repository,
    )

    connection_id = uuid4()

    service.check_health(
        connection_id,
    )

    repository.get_by_id.assert_called_once_with(
        connection_id,
    )