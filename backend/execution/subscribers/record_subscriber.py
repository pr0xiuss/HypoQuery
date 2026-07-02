from backend.execution.contracts.events.base import ExecutionEvent
from backend.execution.contracts.subscriber import Subscriber


class RecordingSubscriber(Subscriber):
    """
    Test subscriber that records every received event.
    """

    def __init__(self) -> None:
        self.events: list[ExecutionEvent] = []

    def handle(
        self,
        event: ExecutionEvent,
    ) -> None:
        self.events.append(event)