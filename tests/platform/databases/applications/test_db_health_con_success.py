from datetime import UTC, datetime
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch
from uuid import uuid4

from backend.platform.databases.application.db_health_service_impl import (
    DatabaseHealthServiceImpl,
)
from backend.platform.databases.domain.db_connection import (
    DatabaseConnection,
)


@patch(
    "backend.platform.databases.application.db_health_service_impl.psycopg.connect",
)
def test_check_health_success(
    mock_connect,
) -> None:
    repository = Mock()

    connection = Mock(
        spec=DatabaseConnection,
    )

    connection.host = "localhost"
    connection.port = 5432
    connection.database_name = "postgres"
    connection.username = "postgres"
    connection.password = "password"

    repository.get_by_id.return_value = connection

    cursor = MagicMock()

    cursor.fetchone.return_value = [
        "16.4",
    ]

    db = MagicMock()

    db.cursor.return_value.__enter__.return_value = cursor

    mock_connect.return_value.__enter__.return_value = db

    service = DatabaseHealthServiceImpl(
        repository,
    )

    result = service.check_health(
        uuid4(),
    )

    assert result.healthy is True
    assert result.postgres_version == "16.4"
    assert result.error is None