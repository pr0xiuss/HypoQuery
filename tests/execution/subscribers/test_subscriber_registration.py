from backend.execution.bootstrap.subscriber_registration import (
    register_execution_subscribers,
)
from backend.execution.bus.subscriber_registry import (
    SubscriberRegistry,
)
from backend.execution.contracts.events import (
    NodeCompletedEvent,
    NodeFailedEvent,
    NodeStartedEvent,
    PipelineCompletedEvent,
    PipelineFailedEvent,
    PipelineStartedEvent,
    QueueDequeuedEvent,
    QueueEnqueuedEvent,
    WorkerAssignedEvent,
    WorkerReleasedEvent,
)


def test_pipeline_subscribers_registered():
    registry = SubscriberRegistry()

    register_execution_subscribers(registry)

    assert len(
        registry.subscribers_for(PipelineStartedEvent)
    ) == 3

    assert len(
        registry.subscribers_for(PipelineCompletedEvent)
    ) == 3

    assert len(
        registry.subscribers_for(PipelineFailedEvent)
    ) == 3


def test_node_subscribers_registered():
    registry = SubscriberRegistry()

    register_execution_subscribers(registry)

    assert len(
        registry.subscribers_for(NodeStartedEvent)
    ) == 3

    assert len(
        registry.subscribers_for(NodeCompletedEvent)
    ) == 3

    assert len(
        registry.subscribers_for(NodeFailedEvent)
    ) == 3


def test_queue_subscribers_registered():
    registry = SubscriberRegistry()

    register_execution_subscribers(registry)

    assert len(
        registry.subscribers_for(QueueEnqueuedEvent)
    ) == 2

    assert len(
        registry.subscribers_for(QueueDequeuedEvent)
    ) == 2


def test_worker_subscribers_registered():
    registry = SubscriberRegistry()

    register_execution_subscribers(registry)

    assert len(
        registry.subscribers_for(WorkerAssignedEvent)
    ) == 2

    assert len(
        registry.subscribers_for(WorkerReleasedEvent)
    ) == 2