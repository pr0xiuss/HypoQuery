from dataclasses import dataclass

from backend.execution.contracts.events.base import WorkerEvent


@dataclass(frozen=True, slots=True)
class WorkerAssignedEvent(WorkerEvent):
    """
    Published when a worker accepts an execution.
    """


@dataclass(frozen=True, slots=True)
class WorkerReleasedEvent(WorkerEvent):
    """
    Published when a worker finishes processing an execution.
    """