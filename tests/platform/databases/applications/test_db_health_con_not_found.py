from unittest.mock import Mock
from uuid import uuid4

from backend.platform.databases.application.db_health_service_impl import (
    DatabaseHealthServiceImpl,
)


def test_check_health_returns_unhealthy_when_connection_not_found() -> None:
    repository = Mock()

    repository.get_by_id.return_value = None

    service = DatabaseHealthServiceImpl(
        repository,
    )

    result = service.check_health(
        uuid4(),
    )

    assert result.healthy is False
    assert result.latency_ms == 0
    assert result.postgres_version is None
    assert result.error == "Database connection not found."