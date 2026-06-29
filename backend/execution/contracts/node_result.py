from dataclasses import dataclass, field
from typing import Any

from .enums import NodeStatus


@dataclass(slots=True)
class NodeResult:
    """
    Represents the outcome of a pipeline node execution.
    """

    status: NodeStatus

    message: str = ""

    next_node: str | None = None

    metadata: dict[str, Any] = field(default_factory=dict)