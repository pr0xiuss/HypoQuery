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
from backend.execution.events.execution_event_factory import (
    ExecutionEventFactory,
)
from backend.execution.events.execution_event_metadata_provider import (
    ExecutionEventMetadataProvider,
)
from tests.execution.events.test_execution_event_metadata_provider import (
    build_execution,
)


def test_pipeline_events() -> None:
    execution = build_execution()

    factory = ExecutionEventFactory(
        ExecutionEventMetadataProvider(),
    )

    assert isinstance(
        factory.pipeline_started(execution),
        PipelineStartedEvent,
    )

    assert isinstance(
        factory.pipeline_completed(execution, 100),
        PipelineCompletedEvent,
    )

    assert isinstance(
        factory.pipeline_failed(execution, "error"),
        PipelineFailedEvent,
    )


def test_node_events() -> None:
    execution = build_execution()

    factory = ExecutionEventFactory(
        ExecutionEventMetadataProvider(),
    )

    assert isinstance(
        factory.node_started(execution, "ParseNode"),
        NodeStartedEvent,
    )

    assert isinstance(
        factory.node_completed(execution, "ParseNode", 25.5),
        NodeCompletedEvent,
    )

    assert isinstance(
        factory.node_failed(
            execution,
            "ParseNode",
            "failure",
        ),
        NodeFailedEvent,
    )


def test_queue_events() -> None:
    execution = build_execution()

    factory = ExecutionEventFactory(
        ExecutionEventMetadataProvider(),
    )

    assert isinstance(
        factory.queue_enqueued(execution),
        QueueEnqueuedEvent,
    )

    assert isinstance(
        factory.queue_dequeued(execution),
        QueueDequeuedEvent,
    )


def test_worker_events() -> None:
    execution = build_execution()

    factory = ExecutionEventFactory(
        ExecutionEventMetadataProvider(),
    )

    assert isinstance(
        factory.worker_assigned(execution, "worker-1"),
        WorkerAssignedEvent,
    )

    assert isinstance(
        factory.worker_released(execution, "worker-1"),
        WorkerReleasedEvent,
    )


def test_sequence_numbers_increment() -> None:
    execution = build_execution()

    factory = ExecutionEventFactory(
        ExecutionEventMetadataProvider(),
    )

    first = factory.pipeline_started(execution)
    second = factory.pipeline_completed(execution, 100)

    assert first.metadata.sequence_number == 1
    assert second.metadata.sequence_number == 2