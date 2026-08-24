import logging
from backend.execution.bus.event_bus import EventBus
from backend.execution.bus.subscriber_registry import SubscriberRegistry
from backend.execution.contracts.events.base import ExecutionEvent

logger = logging.getLogger(__name__)

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
            except Exception as e:
                logger.error(
                    f"Subscriber {subscriber.__class__.__name__} failed to handle event {event.__class__.__name__}: {e}",
                    exc_info=True
                )
                continue