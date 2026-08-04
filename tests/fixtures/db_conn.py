from datetime import UTC
from datetime import datetime
from uuid import uuid4

import pytest

from backend.platform.databases.infra.db_connection_model import (
    DatabaseConnectionModel,
)


@pytest.fixture
def database_connection(
    db_session,
    environment,
) -> DatabaseConnectionModel:
    connection = DatabaseConnectionModel(
        id=uuid4(),
        environment_id=environment.id,
        name="Local PostgreSQL",
        host="localhost",
        port=5432,
        database_name="postgres",
        username="postgres",
        password="pr0xy",
        ssl_enabled=False,
        is_active=True,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )

    db_session.add(
        connection,
    )
    db_session.commit()
    db_session.refresh(
        connection,
    )

    return connection