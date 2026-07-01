from abc import ABC, abstractmethod

from backend.execution.contracts.events import ExecutionEvent


class Publisher(ABC):

    @abstractmethod
    def publish(self, event: ExecutionEvent) -> None:
        """
        Publish an execution event.
        """
        ...