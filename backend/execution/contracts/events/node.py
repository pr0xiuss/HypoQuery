from dataclasses import dataclass
from typing import Optional

from backend.execution.contracts.events.base import NodeEvent


@dataclass(frozen=True, slots=True)
class NodeStartedEvent(NodeEvent):
    """
    Published before a node begins execution.
    """


@dataclass(frozen=True, slots=True)
class NodeCompletedEvent(NodeEvent):
    """
    Published after a node completes successfully.
    """

    duration_ms: float


@dataclass(frozen=True, slots=True)
class NodeFailedEvent(NodeEvent):
    """
    Published when node execution fails.
    """

    error: str
    duration_ms: Optional[float] = None