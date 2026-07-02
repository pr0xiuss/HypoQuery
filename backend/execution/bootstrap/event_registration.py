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
from backend.execution.contracts.subscriber import (
    Subscriber,
)


def subscribe_to_execution_events(
    registry: SubscriberRegistry,
    subscriber: Subscriber,
) -> None:
    """
    Subscribe a subscriber to every execution event.
    """

    registry.subscribe(
        PipelineStartedEvent,
        subscriber,
    )

    registry.subscribe(
        PipelineCompletedEvent,
        subscriber,
    )

    registry.subscribe(
        PipelineFailedEvent,
        subscriber,
    )

    registry.subscribe(
        NodeStartedEvent,
        subscriber,
    )

    registry.subscribe(
        NodeCompletedEvent,
        subscriber,
    )

    registry.subscribe(
        NodeFailedEvent,
        subscriber,
    )

    registry.subscribe(
        QueueEnqueuedEvent,
        subscriber,
    )

    registry.subscribe(
        QueueDequeuedEvent,
        subscriber,
    )

    registry.subscribe(
        WorkerAssignedEvent,
        subscriber,
    )

    registry.subscribe(
        WorkerReleasedEvent,
        subscriber,
    )