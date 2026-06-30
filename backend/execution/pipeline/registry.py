from __future__ import annotations

from .base_node import PipelineNode


class NodeRegistry:
    """
    Registry for all available pipeline nodes.

    Responsible for registering and retrieving node implementations.
    """

    def __init__(self) -> None:
        self._nodes: dict[str, PipelineNode] = {}

    def register(self, node: PipelineNode) -> None:
        """
        Register a node instance.
        """
        if node.name in self._nodes:
            raise ValueError(f"Node '{node.name}' is already registered.")

        self._nodes[node.name] = node

    def get(self, name: str) -> PipelineNode:
        """
        Retrieve a registered node.
        """
        try:
            return self._nodes[name]
        except KeyError as exc:
            raise ValueError(f"Unknown node '{name}'.") from exc

    def contains(self, name: str) -> bool:
        return name in self._nodes

    def all(self) -> tuple[PipelineNode, ...]:
        return tuple(self._nodes.values())
    
    def names(self) -> tuple[str, ...]:
        return tuple(self._nodes.keys())