from abc import ABC, abstractmethod

from backend.execution.contracts.events import ExecutionEvent


class Subscriber(ABC):

    @abstractmethod
    def handle(self, event: ExecutionEvent) -> None:
        """
        Handle an execution event.
        """
        ...