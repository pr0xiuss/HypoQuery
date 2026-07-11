from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from backend.assistant.contracts.assistant_request import (
    AssistantRequest,
)
from backend.assistant.contracts.assistant_response import (
    AssistantResponse,
)


class AssistantFacade(ABC):
    """
    Public entry point exposed by the
    Assistant Platform.
    """

    @abstractmethod
    def explain(
        self,
        request: AssistantRequest,
    ) -> AssistantResponse:
        """
        Generate an explanation for the
        supplied optimization report.
        """