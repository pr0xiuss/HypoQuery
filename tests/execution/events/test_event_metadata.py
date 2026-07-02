from datetime import UTC, datetime
from uuid import uuid4

from backend.execution.contracts.events.enums import EventVersion
from backend.execution.events.metadata import EventMetadata


def test_event_metadata_creation() -> None:
    metadata = EventMetadata(
        event_id=uuid4(),
        execution_id=uuid4(),
        trace_id=uuid4(),
        sequence_number=1,
        timestamp=datetime.now(UTC),
        event_version=EventVersion.V1,
    )

    assert metadata.sequence_number == 1
    assert metadata.event_version == EventVersion.V1


def test_event_metadata_is_immutable() -> None:
    metadata = EventMetadata(
        event_id=uuid4(),
        execution_id=uuid4(),
        trace_id=uuid4(),
        sequence_number=1,
        timestamp=datetime.now(UTC),
        event_version=EventVersion.V1,
    )

    try:
        metadata.sequence_number = 2
        assert False
    except Exception:
        assert True