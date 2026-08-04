from unittest.mock import Mock
from unittest.mock import patch
from uuid import uuid4

import psycopg

from backend.platform.databases.application.db_health_service_impl import (
    DatabaseHealthServiceImpl,
)
from backend.platform.databases.domain.db_connection import (
    DatabaseConnection,
)


@patch(
    "backend.platform.databases.application.db_health_service_impl.psycopg.connect",
)
def test_check_health_returns_unhealthy_on_database_error(
    mock_connect,
) -> None:
    repository = Mock()

    connection = Mock(spec=DatabaseConnection)

    connection.host = "localhost"
    connection.port = 5432
    connection.database_name = "postgres"
    connection.username = "postgres"
    connection.password = "password"

    repository.get_by_id.return_value = connection

    mock_connect.side_effect = psycopg.OperationalError(
        "authentication failed",
    )

    service = DatabaseHealthServiceImpl(
        repository,
    )

    result = service.check_health(
        uuid4(),
    )

    assert result.healthy is False
    assert result.postgres_version is None
    assert "authentication failed" in result.error