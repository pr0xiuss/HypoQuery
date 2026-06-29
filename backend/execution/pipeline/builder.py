from __future__ import annotations

from backend.execution.contracts.exceptions import PipelineValidationError

from .definition import PipelineDefinition
from .pipeline import Pipeline
from .registry import NodeRegistry


class PipelineBuilder:
    """
    Builds validated Pipeline instances.
    """

    def __init__(self, registry: NodeRegistry):
        self._registry = registry

    def build(self, definition: PipelineDefinition) -> Pipeline:
        self._validate(definition)

        nodes = {
            node.name: self._registry.get(node.name)
            for node in definition.nodes
        }

        return Pipeline(
            definition=definition,
            nodes=nodes,
        )

    def _validate(self, definition: PipelineDefinition) -> None:
        """
        Validate the pipeline definition before construction.
        """

        registered = set(self._registry.names())

        # Validate nodes
        for node in definition.nodes:
            if node.name not in registered:
                raise PipelineValidationError(
                    f"Node '{node.name}' is not registered."
                )

        # Validate entry node
        if (
            definition.entry_node is not None
            and definition.entry_node not in registered
        ):
            raise PipelineValidationError(
                f"Entry node '{definition.entry_node}' is not registered."
            )

        # Validate edges
        for source, destinations in definition.edges.items():
            if source not in registered:
                raise PipelineValidationError(
                    f"Unknown source node '{source}'."
                )

            for destination in destinations:
                if destination not in registered:
                    raise PipelineValidationError(
                        f"Unknown destination node '{destination}'."
                    )