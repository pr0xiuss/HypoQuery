from backend.execution.bus.subscriber_registry import SubscriberRegistry

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

from backend.execution.subscribers.logging_subscriber import (
    LoggingSubscriber,
)
from backend.execution.subscribers.metrics_subscriber import (
    MetricsSubscriber,
)
from backend.execution.subscribers.tracing_subscriber import (
    TracingSubscriber,
)


def register_execution_subscribers(
    registry: SubscriberRegistry,
) -> None:
    """
    Register the default execution subscribers.
    """

    logging_subscriber = LoggingSubscriber()
    metrics_subscriber = MetricsSubscriber()
    tracing_subscriber = TracingSubscriber()

    # Logging
    registry.subscribe(
        PipelineStartedEvent,
        logging_subscriber,
    )
    registry.subscribe(
        PipelineCompletedEvent,
        logging_subscriber,
    )
    registry.subscribe(
        PipelineFailedEvent,
        logging_subscriber,
    )
    registry.subscribe(
        NodeStartedEvent,
        logging_subscriber,
    )
    registry.subscribe(
        NodeCompletedEvent,
        logging_subscriber,
    )
    registry.subscribe(
        NodeFailedEvent,
        logging_subscriber,
    )
    registry.subscribe(
        QueueEnqueuedEvent,
        logging_subscriber,
    )
    registry.subscribe(
        QueueDequeuedEvent,
        logging_subscriber,
    )
    registry.subscribe(
        WorkerAssignedEvent,
        logging_subscriber,
    )
    registry.subscribe(
        WorkerReleasedEvent,
        logging_subscriber,
    )

    # Metrics
    registry.subscribe(
        PipelineStartedEvent,
        metrics_subscriber,
    )
    registry.subscribe(
        PipelineCompletedEvent,
        metrics_subscriber,
    )
    registry.subscribe(
        PipelineFailedEvent,
        metrics_subscriber,
    )
    registry.subscribe(
        NodeStartedEvent,
        metrics_subscriber,
    )
    registry.subscribe(
        NodeCompletedEvent,
        metrics_subscriber,
    )
    registry.subscribe(
        NodeFailedEvent,
        metrics_subscriber,
    )

    # Tracing
    registry.subscribe(
        PipelineStartedEvent,
        tracing_subscriber,
    )
    registry.subscribe(
        PipelineCompletedEvent,
        tracing_subscriber,
    )
    registry.subscribe(
        PipelineFailedEvent,
        tracing_subscriber,
    )
    registry.subscribe(
        NodeStartedEvent,
        tracing_subscriber,
    )
    registry.subscribe(
        NodeCompletedEvent,
        tracing_subscriber,
    )
    registry.subscribe(
        NodeFailedEvent,
        tracing_subscriber,
    )
    registry.subscribe(
        QueueEnqueuedEvent,
        tracing_subscriber,
    )
    registry.subscribe(
        QueueDequeuedEvent,
        tracing_subscriber,
    )
    registry.subscribe(
        WorkerAssignedEvent,
        tracing_subscriber,
    )
    registry.subscribe(
        WorkerReleasedEvent,
        tracing_subscriber,
    )