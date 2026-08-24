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

from backend.execution.projections.execution_projection_store import (
    ExecutionProjectionStore,
)
from backend.execution.projections.projection_builder import (
    ProjectionBuilder,
)
from backend.execution.projections.projection_subscriber import (
    ProjectionSubscriber,
)
from .event_registration import (
    subscribe_to_execution_events,
)

def register_execution_subscribers(
    registry: SubscriberRegistry,
    projection_store: ExecutionProjectionStore = None,
) -> None:
    """
    Register the default execution subscribers.
    """

    logging_subscriber = LoggingSubscriber()
    metrics_subscriber = MetricsSubscriber()
    tracing_subscriber = TracingSubscriber()

    if projection_store is None:
        projection_store = ExecutionProjectionStore()

    projection_builder = ProjectionBuilder(
        projection_store,
    )

    projection_subscriber = ProjectionSubscriber(
        projection_builder,
    )

    # Logging
    subscribe_to_execution_events(
        registry,
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
    subscribe_to_execution_events(
        registry,
        tracing_subscriber,
    )



    registry.subscribe(
        PipelineStartedEvent,
        projection_subscriber,
    )

    registry.subscribe(
        PipelineCompletedEvent,
        projection_subscriber,
    )

    registry.subscribe(
        PipelineFailedEvent,
        projection_subscriber,
    )

    registry.subscribe(
        NodeStartedEvent,
        projection_subscriber,
    )

    registry.subscribe(
        NodeCompletedEvent,
        projection_subscriber,
    )

    registry.subscribe(
        NodeFailedEvent,
        projection_subscriber,
    )

    registry.subscribe(
        QueueEnqueuedEvent,
        projection_subscriber,
    )

    registry.subscribe(
        WorkerAssignedEvent,
        projection_subscriber,
    )