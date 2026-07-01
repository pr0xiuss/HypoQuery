from backend.execution.contracts.execution import PipelineExecution
from backend.execution.contracts.events.base import ExecutionEvent
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
    QueueDequeuedEvent,
    QueueEnqueuedEvent,
)
from backend.execution.contracts.events.worker import (
    WorkerAssignedEvent,
    WorkerReleasedEvent,
)
from backend.execution.events.execution_event_metadata_provider import (
    ExecutionEventMetadataProvider,
)


class ExecutionEventFactory:
    """
    Creates immutable execution events.
    """

    def __init__(
        self,
        metadata_provider: ExecutionEventMetadataProvider,
    ) -> None:
        self._metadata_provider = metadata_provider

    def pipeline_started(
        self,
        execution: PipelineExecution,
    ) -> PipelineStartedEvent:
        return PipelineStartedEvent(
            metadata=self._metadata_provider.create(execution),
        )

    def pipeline_completed(
        self,
        execution: PipelineExecution,
        duration_ms: float,
    ) -> PipelineCompletedEvent:
        return PipelineCompletedEvent(
            metadata=self._metadata_provider.create(execution),
            duration_ms=duration_ms,
        )

    def pipeline_failed(
        self,
        execution: PipelineExecution,
        error: str,
        duration_ms: float | None = None,
    ) -> PipelineFailedEvent:
        return PipelineFailedEvent(
            metadata=self._metadata_provider.create(execution),
            error=error,
            duration_ms=duration_ms,
        )

    def node_started(
        self,
        execution: PipelineExecution,
        node_name: str,
    ) -> NodeStartedEvent:
        return NodeStartedEvent(
            metadata=self._metadata_provider.create(execution),
            node_name=node_name,
        )

    def node_completed(
        self,
        execution: PipelineExecution,
        node_name: str,
        duration_ms: float,
    ) -> NodeCompletedEvent:
        return NodeCompletedEvent(
            metadata=self._metadata_provider.create(execution),
            node_name=node_name,
            duration_ms=duration_ms,
        )

    def node_failed(
        self,
        execution: PipelineExecution,
        node_name: str,
        error: str,
    ) -> NodeFailedEvent:
        return NodeFailedEvent(
            metadata=self._metadata_provider.create(execution),
            node_name=node_name,
            error=error,
        )

    def queue_enqueued(
        self,
        execution: PipelineExecution,
    ) -> QueueEnqueuedEvent:
        return QueueEnqueuedEvent(
            metadata=self._metadata_provider.create(execution),
        )

    def queue_dequeued(
        self,
        execution: PipelineExecution,
    ) -> QueueDequeuedEvent:
        return QueueDequeuedEvent(
            metadata=self._metadata_provider.create(execution),
        )

    def worker_assigned(
        self,
        execution: PipelineExecution,
        worker_id: str,
    ) -> WorkerAssignedEvent:
        return WorkerAssignedEvent(
            metadata=self._metadata_provider.create(execution),
            worker_id=worker_id,
        )

    def worker_released(
        self,
        execution: PipelineExecution,
        worker_id: str,
    ) -> WorkerReleasedEvent:
        return WorkerReleasedEvent(
            metadata=self._metadata_provider.create(execution),
            worker_id=worker_id,
        )