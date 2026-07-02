from datetime import UTC, datetime
from uuid import uuid4

from backend.execution.contracts.events.enums import EventVersion
from backend.execution.contracts.events.pipeline import (
    PipelineCompletedEvent,
    PipelineStartedEvent,
)
from backend.execution.events.metadata import EventMetadata
from backend.execution.lifecycle.enums import ExecutionStatus

from backend.execution.projections.execution_projection_store import (
    ExecutionProjectionStore,
)
from backend.execution.projections.projection_builder import (
    ProjectionBuilder,
)


def metadata():
    return EventMetadata(
        event_id=uuid4(),
        execution_id=uuid4(),
        trace_id=uuid4(),
        sequence_number=1,
        timestamp=datetime.now(UTC),
        event_version=EventVersion.V1,
    )


def test_projection_flow():
    store = ExecutionProjectionStore()

    builder = ProjectionBuilder(
        store,
    )

    meta = metadata()

    builder.apply(
        PipelineStartedEvent(
            metadata=meta,
        )
    )

    builder.apply(
        PipelineCompletedEvent(
            metadata=meta,
            duration_ms=150,
        )
    )

    projection = store.get(
        meta.execution_id,
    )

    assert projection is not None
    assert projection.status == ExecutionStatus.COMPLETED
    assert projection.duration_ms == 150
    assert projection.started_at is not None
    assert projection.completed_at is not None