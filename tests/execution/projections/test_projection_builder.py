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
from backend.execution.contracts.events.queue import (
    QueueEnqueuedEvent,
)
from backend.execution.contracts.events.worker import (
    WorkerAssignedEvent,
)
from backend.execution.lifecycle.enums import ExecutionStatus
from backend.execution.events.metadata import EventMetadata

from backend.execution.projections.execution_projection_store import (
    ExecutionProjectionStore,
)
from backend.execution.projections.projection_builder import (
    ProjectionBuilder,
)


EXECUTION_ID = uuid4()
TRACE_ID = uuid4()


def metadata() -> EventMetadata:
    return EventMetadata(
        event_id=uuid4(),
        execution_id=EXECUTION_ID,
        trace_id=TRACE_ID,
        sequence_number=1,
        timestamp=datetime.now(UTC),
        event_version=EventVersion.V1,
    )


def build_builder():
    store = ExecutionProjectionStore()
    builder = ProjectionBuilder(store)

    return builder, store


def test_pipeline_started_projection():
    builder, store = build_builder()

    builder.apply(
        PipelineStartedEvent(
            metadata=metadata(),
        )
    )

    projection = store.get(EXECUTION_ID)

    assert projection is not None
    assert projection.status == ExecutionStatus.RUNNING
    assert projection.started_at is not None


def test_pipeline_completed_projection():
    builder, store = build_builder()

    builder.apply(
        PipelineCompletedEvent(
            metadata=metadata(),
            duration_ms=120.5,
        )
    )

    projection = store.get(EXECUTION_ID)

    assert projection.status == ExecutionStatus.COMPLETED
    assert projection.duration_ms == 120.5
    assert projection.completed_at is not None


def test_pipeline_failed_projection():
    builder, store = build_builder()

    builder.apply(
        PipelineFailedEvent(
            metadata=metadata(),
            error="boom",
            duration_ms=25.0,
        )
    )

    projection = store.get(EXECUTION_ID)

    assert projection.status == ExecutionStatus.FAILED
    assert projection.duration_ms == 25.0


def test_queue_and_worker_projection():
    builder, store = build_builder()

    builder.apply(
        QueueEnqueuedEvent(
            metadata=metadata(),
        )
    )

    builder.apply(
        WorkerAssignedEvent(
            metadata=metadata(),
            worker_id="worker-1",
        )
    )

    projection = store.get(EXECUTION_ID)

    assert projection.status == ExecutionStatus.ASSIGNED
    assert projection.queue_time is not None
    assert projection.assigned_at is not None
    assert projection.assigned_worker == "worker-1"


def test_node_counters():
    builder, store = build_builder()

    builder.apply(
        NodeStartedEvent(
            metadata=metadata(),
            node_name="ParseNode",
        )
    )

    builder.apply(
        NodeCompletedEvent(
            metadata=metadata(),
            node_name="ParseNode",
            duration_ms=10,
        )
    )

    builder.apply(
        NodeFailedEvent(
            metadata=metadata(),
            node_name="ValidateNode",
            error="boom",
        )
    )

    projection = store.get(EXECUTION_ID)

    assert projection.nodes_started == 1
    assert projection.nodes_completed == 1
    assert projection.nodes_failed == 1