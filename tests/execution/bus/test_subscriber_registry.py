from backend.execution.bus.subscriber_registry import SubscriberRegistry
from backend.execution.contracts.events.pipeline import PipelineStartedEvent
# from backend.execution.events.execution_event_metadata_provider import (
#     ExecutionEventMetadataProvider,
# )
from backend.execution.subscribers.record_subscriber import RecordingSubscriber
from tests.execution.events.test_execution_event_metadata_provider import (
    build_execution,
)


def test_register_subscriber() -> None:
    registry = SubscriberRegistry()
    subscriber = RecordingSubscriber()

    registry.subscribe(PipelineStartedEvent, subscriber)

    subscribers = registry.subscribers_for(PipelineStartedEvent)

    assert len(subscribers) == 1
    assert subscribers[0] is subscriber


def test_multiple_subscribers() -> None:
    registry = SubscriberRegistry()

    first = RecordingSubscriber()
    second = RecordingSubscriber()

    registry.subscribe(PipelineStartedEvent, first)
    registry.subscribe(PipelineStartedEvent, second)

    subscribers = registry.subscribers_for(PipelineStartedEvent)

    assert len(subscribers) == 2
    assert first in subscribers
    assert second in subscribers


def test_unknown_event_returns_empty_list() -> None:
    registry = SubscriberRegistry()

    subscribers = registry.subscribers_for(PipelineStartedEvent)

    assert subscribers == []