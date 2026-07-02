from datetime import UTC, datetime
from uuid import uuid4

from backend.execution.contracts.events.enums import EventVersion
from backend.execution.contracts.events.node import (
    NodeCompletedEvent,
    NodeFailedEvent,
    NodeStartedEvent,
)
from backend.execution.contracts.events.pipeline import (
    PipelineCompletedEvent,
    PipelineFailedEvent,
    PipelineStartedEvent,
)
from backend.execution.events.metadata import EventMetadata
from backend.execution.subscribers.metrics_subscriber import (
    MetricsSubscriber,
)


def metadata() -> EventMetadata:
    return EventMetadata(
        event_id=uuid4(),
        execution_id=uuid4(),
        trace_id=uuid4(),
        sequence_number=1,
        timestamp=datetime.now(UTC),
        event_version=EventVersion.V1,
    )


def test_pipeline_metrics():
    subscriber = MetricsSubscriber()

    subscriber.handle(
        PipelineStartedEvent(
            metadata=metadata(),
        )
    )

    subscriber.handle(
        PipelineCompletedEvent(
            metadata=metadata(),
            duration_ms=100.0,
        )
    )

    metrics = subscriber.metrics

    assert metrics["pipelines_started"] == 1
    assert metrics["pipelines_completed"] == 1
    assert metrics["pipelines_failed"] == 0


def test_node_metrics():
    subscriber = MetricsSubscriber()

    subscriber.handle(
        NodeStartedEvent(
            metadata=metadata(),
            node_name="ParseNode",
        )
    )

    subscriber.handle(
        NodeCompletedEvent(
            metadata=metadata(),
            node_name="ParseNode",
            duration_ms=10.0,
        )
    )

    subscriber.handle(
        NodeFailedEvent(
            metadata=metadata(),
            node_name="ParseNode",
            error="boom",
        )
    )

    metrics = subscriber.metrics

    assert metrics["nodes_started"] == 1
    assert metrics["nodes_completed"] == 1
    assert metrics["nodes_failed"] == 1


def test_clear():
    subscriber = MetricsSubscriber()

    subscriber.handle(
        PipelineStartedEvent(
            metadata=metadata(),
        )
    )

    subscriber.clear()

    assert all(
        value == 0
        for value in subscriber.metrics.values()
    )