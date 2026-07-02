from backend.execution.bus.in_process_event_bus import InProcessEventBus
from backend.execution.bus.subscriber_registry import SubscriberRegistry
from backend.execution.contracts.events.pipeline import PipelineStartedEvent
from backend.execution.events.execution_event_metadata_provider import (
    ExecutionEventMetadataProvider,
)
from backend.execution.subscribers.record_subscriber import RecordingSubscriber
from tests.execution.events.test_execution_event_metadata_provider import (
    build_execution,
)


class FailingSubscriber(RecordingSubscriber):
    def handle(self, event):
        raise RuntimeError("failure")


def build_event() -> PipelineStartedEvent:
    execution = build_execution()

    provider = ExecutionEventMetadataProvider()

    return PipelineStartedEvent(
        metadata=provider.create(execution),
    )


def test_publish_to_single_subscriber() -> None:
    registry = SubscriberRegistry()
    subscriber = RecordingSubscriber()

    registry.subscribe(PipelineStartedEvent, subscriber)

    bus = InProcessEventBus(registry)

    event = build_event()

    bus.publish(event)

    assert len(subscriber.events) == 1
    assert subscriber.events[0] is event


def test_publish_to_multiple_subscribers() -> None:
    registry = SubscriberRegistry()

    first = RecordingSubscriber()
    second = RecordingSubscriber()

    registry.subscribe(PipelineStartedEvent, first)
    registry.subscribe(PipelineStartedEvent, second)

    bus = InProcessEventBus(registry)

    event = build_event()

    bus.publish(event)

    assert len(first.events) == 1
    assert len(second.events) == 1


def test_subscriber_failure_does_not_stop_dispatch() -> None:
    registry = SubscriberRegistry()

    failing = FailingSubscriber()
    working = RecordingSubscriber()

    registry.subscribe(PipelineStartedEvent, failing)
    registry.subscribe(PipelineStartedEvent, working)

    bus = InProcessEventBus(registry)

    event = build_event()

    bus.publish(event)

    assert len(working.events) == 1