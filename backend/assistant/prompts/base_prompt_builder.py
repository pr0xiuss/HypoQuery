from __future__ import annotations

from abc import ABC, abstractmethod

from backend.assistant.models.ai_request import (
    AIRequest,
)
from backend.knowledge.models.explanation_snapshot import (
    ExplanationSnapshot,
)


class PromptBuilder(ABC):
    """
    Base contract implemented by every prompt
    builder.
    """

    @abstractmethod
    def build(
        self,
        explanation: ExplanationSnapshot,
    ) -> AIRequest:
        """
        Build an AI request from an explanation
        snapshot.
        """