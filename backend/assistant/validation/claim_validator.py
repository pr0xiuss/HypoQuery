from __future__ import annotations

from backend.assistant.contracts.assistant_response import (
    AssistantResponse,
)
from backend.assistant.validation.base_validator import (
    ResponseValidator,
)


class ClaimValidator(
    ResponseValidator,
):
    """
    Validates that an assistant response
    contains meaningful content.
    """

    def validate(
        self,
        response: AssistantResponse,
    ) -> None:

        if not response.result.content.strip():

            raise ValueError(
                "Assistant response is empty."
            )