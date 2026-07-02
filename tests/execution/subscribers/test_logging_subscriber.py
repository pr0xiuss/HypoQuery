from uuid import uuid4

from backend.execution.contracts.events.enums import EventVersion
from backend.execution.contracts.events.pipeline import (
    PipelineStartedEvent,
)
from backend.execution.events.metadata import EventMetadata
from backend.execution.subscribers.logging_subscriber import (
    LoggingSubscriber,
)
from datetime import UTC, datetime

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


def test_stores_events():
    subscriber = LoggingSubscriber()

    event = make_event()

    subscriber.handle(event)

    assert subscriber.events == [event]


def test_returns_copy():
    subscriber = LoggingSubscriber()

    subscriber.handle(make_event())

    events = subscriber.events

    events.clear()

    assert len(subscriber.events) == 1


def test_clear():
    subscriber = LoggingSubscriber()

    subscriber.handle(make_event())

    subscriber.clear()

    assert subscriber.events == []