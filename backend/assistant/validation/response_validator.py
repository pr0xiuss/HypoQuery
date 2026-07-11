from __future__ import annotations

from backend.assistant.contracts.assistant_response import (
    AssistantResponse,
)
from backend.assistant.validation.base_validator import (
    ResponseValidator,
)
from backend.assistant.validation.validation_pipeline import (
    ValidationPipeline,
)


class CompositeResponseValidator(
    ResponseValidator,
):
    """
    Coordinates all assistant response
    validators.
    """

    def __init__(
        self,
        pipeline: ValidationPipeline,
    ) -> None:

        self._pipeline = pipeline

    def validate(
        self,
        response: AssistantResponse,
    ) -> None:

        self._pipeline.validate(
            response,
        )