from collections import defaultdict
from typing import Type

from backend.execution.contracts.events.base import ExecutionEvent
from backend.execution.contracts.subscriber import Subscriber


class SubscriberRegistry:
    """
    Maintains event type to subscriber mappings.
    """

    def __init__(self) -> None:
        self._subscriptions: dict[
            Type[ExecutionEvent],
            list[Subscriber],
        ] = defaultdict(list)

    def subscribe(
        self,
        event_type: Type[ExecutionEvent],
        subscriber: Subscriber,
    ) -> None:
        self._subscriptions[event_type].append(subscriber)

    def subscribers_for(
        self,
        event_type: Type[ExecutionEvent],
    ) -> list[Subscriber]:
        return list(self._subscriptions.get(event_type, []))