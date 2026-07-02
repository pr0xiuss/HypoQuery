from backend.execution.contracts.events import (
    NodeCompletedEvent,
    NodeFailedEvent,
    NodeStartedEvent,
    PipelineCompletedEvent,
    PipelineFailedEvent,
    PipelineStartedEvent,
    QueueEnqueuedEvent,
    WorkerAssignedEvent,
)
from backend.execution.lifecycle.enums import ExecutionStatus

from .execution_projection import ExecutionProjection
from .execution_projection_store import ExecutionProjectionStore


class ProjectionBuilder:
    """
    Builds and updates execution projections from execution events.
    """

    def __init__(
        self,
        store: ExecutionProjectionStore,
    ) -> None:
        self._store = store

    def apply(
        self,
        event,
    ) -> None:

        projection = self._store.get(
            event.metadata.execution_id,
        )

        if projection is None:
            projection = ExecutionProjection(
                execution_id=event.metadata.execution_id,
                trace_id=event.metadata.trace_id,
            )

        if isinstance(event, QueueEnqueuedEvent):
            projection.queue_time = event.metadata.timestamp
            projection.status = ExecutionStatus.QUEUED

        elif isinstance(event, WorkerAssignedEvent):
            projection.assigned_at = event.metadata.timestamp
            projection.assigned_worker = event.worker_id
            projection.status = ExecutionStatus.ASSIGNED

        elif isinstance(event, PipelineStartedEvent):
            projection.started_at = event.metadata.timestamp
            projection.status = ExecutionStatus.RUNNING

        elif isinstance(event, PipelineCompletedEvent):
            projection.completed_at = event.metadata.timestamp
            projection.duration_ms = event.duration_ms
            projection.status = ExecutionStatus.COMPLETED

        elif isinstance(event, PipelineFailedEvent):
            projection.completed_at = event.metadata.timestamp
            projection.duration_ms = event.duration_ms
            projection.status = ExecutionStatus.FAILED

        elif isinstance(event, NodeStartedEvent):
            projection.nodes_started += 1

        elif isinstance(event, NodeCompletedEvent):
            projection.nodes_completed += 1

        elif isinstance(event, NodeFailedEvent):
            projection.nodes_failed += 1

        self._store.save(
            projection,
        )