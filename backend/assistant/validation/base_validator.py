from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from backend.assistant.contracts.assistant_response import (
    AssistantResponse,
)


class ResponseValidator(ABC):
    """
    Base contract implemented by every
    assistant response validator.
    """

    @abstractmethod
    def validate(
        self,
        response: AssistantResponse,
    ) -> None:
        """
        Validate an assistant response.

        Raises an exception if validation
        fails.
        """