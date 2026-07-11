from __future__ import annotations

from backend.assistant.api.assistant_facade import (
    AssistantFacade,
)
from backend.assistant.contracts.assistant_request import (
    AssistantRequest,
)
from backend.assistant.contracts.assistant_response import (
    AssistantResponse,
)


class AssistantPlatform:
    """
    Public entry point for the Assistant
    Platform.
    """

    def __init__(
        self,
        assistant: AssistantFacade,
    ) -> None:

        self._assistant = assistant

    def explain(
        self,
        request: AssistantRequest,
    ) -> AssistantResponse:

        return self._assistant.explain(
            request,
        )