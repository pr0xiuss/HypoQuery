from abc import ABC, abstractmethod

from backend.execution.contracts.events.base import ExecutionEvent


class EventBus(ABC):
    """
    Dispatches execution events to subscribers.
    """

    @abstractmethod
    def publish(
        self,
        event: ExecutionEvent,
    ) -> None:
        pass