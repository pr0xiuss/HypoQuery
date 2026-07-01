from backend.execution.bus.in_process_event_bus import InProcessEventBus
from backend.execution.bus.subscriber_registry import SubscriberRegistry
from backend.execution.contracts.events.pipeline import PipelineStartedEvent
from backend.execution.events.execution_event_metadata_provider import (
    ExecutionEventMetadataProvider,
)
from backend.execution.publisher.event_publisher import EventPublisher
from backend.execution.subscribers.record_subscriber import RecordingSubscriber
from tests.execution.events.test_execution_event_metadata_provider import (
    build_execution,
)


def build_event() -> PipelineStartedEvent:
    execution = build_execution()

    provider = ExecutionEventMetadataProvider()

    return PipelineStartedEvent(
        metadata=provider.create(execution),
    )


def test_publisher_delegates_to_event_bus() -> None:
    registry = SubscriberRegistry()
    subscriber = RecordingSubscriber()

    registry.subscribe(PipelineStartedEvent, subscriber)

    bus = InProcessEventBus(registry)

    publisher = EventPublisher(bus)

    event = build_event()

    publisher.publish(event)

    assert len(subscriber.events) == 1
    assert subscriber.events[0] is event


def test_publisher_does_not_modify_event() -> None:
    registry = SubscriberRegistry()

    bus = InProcessEventBus(registry)

    publisher = EventPublisher(bus)

    event = build_event()

    original_id = event.metadata.event_id

    publisher.publish(event)

    assert event.metadata.event_id == original_id