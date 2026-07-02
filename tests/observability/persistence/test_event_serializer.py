from datetime import UTC, datetime
from uuid import uuid4

from backend.execution.contracts.events.enums import EventVersion
from backend.execution.contracts.events.pipeline import (
    PipelineStartedEvent,
)
from backend.execution.events.metadata import EventMetadata

from backend.observability.persistence.event_serializer import (
    EventSerializer,
)


def make_event() -> PipelineStartedEvent:
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


def test_serializes_event():
    serializer = EventSerializer()

    payload = serializer.serialize(
        make_event(),
    )

    assert isinstance(payload, dict)

    assert payload["metadata"]["event_id"]
    assert payload["metadata"]["execution_id"]
    assert payload["metadata"]["trace_id"]

    assert payload["metadata"]["sequence_number"] == 1

    assert (payload["metadata"]["event_version"] == EventVersion.V1.value)


def test_serializes_datetime():
    serializer = EventSerializer()

    payload = serializer.serialize(
        make_event(),
    )

    assert isinstance(
        payload["metadata"]["timestamp"],
        str,
    )


def test_serializes_uuid():
    serializer = EventSerializer()

    payload = serializer.serialize(
        make_event(),
    )

    assert isinstance(
        payload["metadata"]["event_id"],
        str,
    )

    assert isinstance(
        payload["metadata"]["execution_id"],
        str,
    )

    assert isinstance(
        payload["metadata"]["trace_id"],
        str,
    )