from backend.execution.contracts.events.base import (
    ExecutionEvent,
)
from backend.execution.contracts.subscriber import Subscriber

from .projection_builder import ProjectionBuilder


class ProjectionSubscriber(Subscriber):
    """
    Updates execution projections from execution events.
    """

    def __init__(
        self,
        builder: ProjectionBuilder,
    ) -> None:
        self._builder = builder

    def handle(
        self,
        event: ExecutionEvent,
    ) -> None:
        self._builder.apply(
            event,
        )