from __future__ import annotations

from backend.execution.contracts.exceptions import PipelineValidationError

from .definition import PipelineDefinition


class PipelineRegistry:
    """
    Registry of pipeline definitions.

    Stores immutable pipeline definitions and allows
    them to be retrieved by pipeline id.
    """

    def __init__(self) -> None:

        self._definitions: dict[str, PipelineDefinition] = {}

    def register(
        self,
        definition: PipelineDefinition,
    ) -> None:
        """
        Register a pipeline definition.
        """

        if definition.pipeline_id in self._definitions:
            raise PipelineValidationError(
                f"Pipeline '{definition.pipeline_id}' is already registered."
            )

        self._definitions[definition.pipeline_id] = definition

    def get(
        self,
        pipeline_id: str,
    ) -> PipelineDefinition:
        """
        Retrieve a pipeline definition.
        """

        try:
            return self._definitions[pipeline_id]

        except KeyError as exc:
            raise PipelineValidationError(
                f"Unknown pipeline '{pipeline_id}'."
            ) from exc

    def contains(
        self,
        pipeline_id: str,
    ) -> bool:
        """
        Check if a pipeline exists.
        """

        return pipeline_id in self._definitions

    def names(
        self,
    ) -> tuple[str, ...]:
        """
        Return all registered pipeline ids.
        """

        return tuple(self._definitions.keys())