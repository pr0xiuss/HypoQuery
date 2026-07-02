from backend.execution.contracts.events.base import (
    ExecutionEvent,
)
from backend.execution.contracts.subscriber import Subscriber

from .event_repository import EventRepository


class PersistenceSubscriber(Subscriber):
    """
    Persists execution events.
    """

    def __init__(
        self,
        repository: EventRepository,
    ) -> None:
        self._repository = repository

    def handle(
        self,
        event: ExecutionEvent,
    ) -> None:
        self._repository.save(
            event,
        )