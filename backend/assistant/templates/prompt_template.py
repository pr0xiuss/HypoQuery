from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from backend.knowledge.models.explanation_snapshot import (
    ExplanationSnapshot,
)


class PromptTemplate(ABC):
    """
    Base contract implemented by every
    prompt template.
    """

    @abstractmethod
    def render(
        self,
        explanation: ExplanationSnapshot,
    ) -> str:
        """
        Render the explanation into the
        template body.
        """