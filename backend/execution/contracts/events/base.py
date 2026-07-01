from dataclasses import dataclass

from backend.execution.events.metadata import EventMetadata


@dataclass(frozen=True, slots=True)
class ExecutionEvent:
    """
    Root immutable execution event.
    """

    metadata: EventMetadata


@dataclass(frozen=True, slots=True)
class PipelineEvent(ExecutionEvent):
    """
    Base class for all pipeline lifecycle events.
    """


@dataclass(frozen=True, slots=True)
class NodeEvent(ExecutionEvent):
    """
    Base class for all node lifecycle events.
    """

    node_name: str


@dataclass(frozen=True, slots=True)
class QueueEvent(ExecutionEvent):
    """
    Base class for all queue lifecycle events.
    """


@dataclass(frozen=True, slots=True)
class WorkerEvent(ExecutionEvent):
    """
    Base class for all worker lifecycle events.
    """

    worker_id: str