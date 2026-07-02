from backend.execution.bus.event_bus import EventBus
from backend.execution.contracts.events.base import ExecutionEvent
from backend.execution.contracts.publisher import Publisher


class EventPublisher(Publisher):
    """
    Publishes execution events through the configured event bus.
    """

    def __init__(
        self,
        event_bus: EventBus,
    ) -> None:
        self._event_bus = event_bus

    def publish(
        self,
        event: ExecutionEvent,
    ) -> None:
        self._event_bus.publish(event)