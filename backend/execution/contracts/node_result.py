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

    @classmethod
    def success(
        cls,
        message: str = "",
        *,
        next_node: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> "NodeResult":

        return cls(
            status=NodeStatus.SUCCESS,
            message=message,
            next_node=next_node,
            metadata=metadata or {},
        )

    @classmethod
    def failure(
        cls,
        message: str,
        *,
        metadata: dict[str, Any] | None = None,
    ) -> "NodeResult":

        return cls(
            status=NodeStatus.FAILED,
            message=message,
            metadata=metadata or {},
        )

    @classmethod
    def skipped(
        cls,
        message: str = "",
    ) -> "NodeResult":

        return cls(
            status=NodeStatus.SKIPPED,
            message=message,
        )