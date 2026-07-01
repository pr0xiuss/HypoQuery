from backend.execution.bus.event_bus import EventBus
from backend.execution.bus.subscriber_registry import SubscriberRegistry
from backend.execution.contracts.events.base import ExecutionEvent


class InProcessEventBus(EventBus):
    """
    Synchronous in-process event bus.
    """

    def __init__(
        self,
        registry: SubscriberRegistry,
    ) -> None:
        self._registry = registry

    def publish(
        self,
        event: ExecutionEvent,
    ) -> None:
        subscribers = self._registry.subscribers_for(type(event))

        for subscriber in subscribers:
            try:
                subscriber.handle(event)
            except Exception:
                continue