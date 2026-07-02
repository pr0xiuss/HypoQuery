from datetime import UTC, datetime
from uuid import uuid4

from backend.execution.contracts.events.enums import EventVersion
from backend.execution.contracts.events.node import (
    NodeCompletedEvent,
)
from backend.execution.contracts.events.pipeline import (
    PipelineStartedEvent,
)
from backend.execution.events.metadata import EventMetadata
from backend.execution.subscribers.tracing_subscriber import (
    TracingSubscriber,
)


def metadata(trace_id=None) -> EventMetadata:
    return EventMetadata(
        event_id=uuid4(),
        execution_id=uuid4(),
        trace_id=trace_id or uuid4(),
        sequence_number=1,
        timestamp=datetime.now(UTC),
        event_version=EventVersion.V1,
    )


def test_groups_events_by_trace():
    subscriber = TracingSubscriber()

    trace_id = uuid4()

    subscriber.handle(
        PipelineStartedEvent(
            metadata=metadata(trace_id),
        )
    )

    subscriber.handle(
        NodeCompletedEvent(
            metadata=metadata(trace_id),
            node_name="ParseNode",
            duration_ms=15.0,
        )
    )

    traces = subscriber.traces

    assert trace_id in traces
    assert len(traces[trace_id]) == 2


def test_separate_traces():
    subscriber = TracingSubscriber()

    trace1 = uuid4()
    trace2 = uuid4()

    subscriber.handle(
        PipelineStartedEvent(
            metadata=metadata(trace1),
        )
    )

    subscriber.handle(
        PipelineStartedEvent(
            metadata=metadata(trace2),
        )
    )

    traces = subscriber.traces

    assert len(traces) == 2


def test_returns_copy():
    subscriber = TracingSubscriber()

    trace_id = uuid4()

    subscriber.handle(
        PipelineStartedEvent(
            metadata=metadata(trace_id),
        )
    )

    traces = subscriber.traces

    traces.clear()

    assert len(subscriber.traces) == 1


def test_clear():
    subscriber = TracingSubscriber()

    subscriber.handle(
        PipelineStartedEvent(
            metadata=metadata(),
        )
    )

    subscriber.clear()

    assert subscriber.traces == {}