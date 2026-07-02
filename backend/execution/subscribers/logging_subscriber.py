from backend.execution.contracts.events import ExecutionEvent
from backend.execution.contracts.subscriber import Subscriber


class LoggingSubscriber(Subscriber):
    """
    Stores execution events in memory.

    Later phases will forward these events to the logging system.
    """

    def __init__(self) -> None:
        self._events: list[ExecutionEvent] = []

    def handle(
        self,
        event: ExecutionEvent,
    ) -> None:
        self._events.append(event)

    @property
    def events(self) -> list[ExecutionEvent]:
        return list(self._events)

    def clear(self) -> None:
        self._events.clear()