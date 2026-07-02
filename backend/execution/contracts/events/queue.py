from dataclasses import dataclass

from backend.execution.contracts.events.base import QueueEvent


@dataclass(frozen=True, slots=True)
class QueueEnqueuedEvent(QueueEvent):
    """
    Published after a pipeline execution is enqueued.
    """


@dataclass(frozen=True, slots=True)
class QueueDequeuedEvent(QueueEvent):
    """
    Published after a pipeline execution is dequeued.
    """