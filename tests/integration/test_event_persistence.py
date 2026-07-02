from datetime import UTC, datetime
from unittest.mock import MagicMock
from uuid import uuid4

from backend.execution.contracts.events.enums import EventVersion
from backend.execution.contracts.events.pipeline import (
    PipelineStartedEvent,
)
from backend.execution.events.metadata import EventMetadata

from backend.observability.persistence.event_repository import (
    EventRepository,
)
from backend.observability.persistence.event_serializer import (
    EventSerializer,
)
from backend.observability.persistence.persistence_subscriber import (
    PersistenceSubscriber,
)


def make_connection():
    connection = MagicMock()

    cursor = MagicMock()

    connection.cursor.return_value.__enter__.return_value = (
        cursor
    )

    return connection, cursor


def make_event():
    return PipelineStartedEvent(
        metadata=EventMetadata(
            event_id=uuid4(),
            execution_id=uuid4(),
            trace_id=uuid4(),
            sequence_number=1,
            timestamp=datetime.now(UTC),
            event_version=EventVersion.V1,
        ),
    )


def test_persistence_flow():
    connection, cursor = make_connection()

    repository = EventRepository(
        connection,
        EventSerializer(),
    )

    subscriber = PersistenceSubscriber(
        repository,
    )

    subscriber.handle(
        make_event(),
    )

    cursor.execute.assert_called_once()

    connection.commit.assert_called_once()