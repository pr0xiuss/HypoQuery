from __future__ import annotations

from backend.assistant.contracts.assistant_response import (
    AssistantResponse,
)
from backend.assistant.validation.base_validator import (
    ResponseValidator,
)


class ValidationPipeline:
    """
    Executes assistant response validators.
    """

    def __init__(
        self,
        validators: list[ResponseValidator],
    ) -> None:

        self._validators = validators

    def validate(
        self,
        response: AssistantResponse,
    ) -> None:

        for validator in self._validators:

            validator.validate(
                response,
            )