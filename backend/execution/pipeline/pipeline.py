from __future__ import annotations

from dataclasses import dataclass, field
from .base_node import PipelineNode
from .definition import PipelineDefinition
from backend.execution.contracts.exceptions import PipelineExecutionError

@dataclass(slots=True)
class Pipeline:
    """
    Runtime representation of a validated pipeline.
    """

    definition: PipelineDefinition

    nodes: dict[str, PipelineNode] = field(default_factory=dict)

    def get_node(self, name: str) -> PipelineNode:
        return self.nodes[name]

    def successors(self, name: str) -> tuple[str, ...]:
        return self.definition.edges.get(name, ())

    def next_node(self, current: str) -> str | None:
        successors = self.successors(current)

        if not successors:
            return None

        if len(successors) > 1:
            raise PipelineExecutionError(
                "Multiple successors require a router."
            )

        return successors[0]

