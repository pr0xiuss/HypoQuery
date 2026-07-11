from __future__ import annotations

from backend.assistant.contracts.assistant_response import (
    AssistantResponse,
)
from backend.assistant.validation.base_validator import (
    ResponseValidator,
)


class CitationValidator(
    ResponseValidator,
):
    """
    Placeholder validator for future
    citation verification.

    Currently accepts every response.
    """

    def validate(
        self,
        response: AssistantResponse,
    ) -> None:

        return