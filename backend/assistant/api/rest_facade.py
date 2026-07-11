from __future__ import annotations

from dataclasses import asdict

from backend.assistant.api.assistant_facade import (
    AssistantFacade,
)
from backend.assistant.contracts.assistant_request import (
    AssistantRequest,
)


class RestFacade:
    """
    Transport adapter used by REST APIs.

    Converts Assistant contracts into
    serializable dictionaries.
    """

    def __init__(
        self,
        assistant: AssistantFacade,
    ) -> None:

        self._assistant = assistant

    def explain(
        self,
        request: AssistantRequest,
    ) -> dict:

        response = self._assistant.explain(
            request,
        )

        return asdict(
            response,
        )