from __future__ import annotations

from dataclasses import dataclass

from backend.knowledge.models.explanation_snapshot import (
    ExplanationSnapshot,
)


@dataclass(
    frozen=True,
    slots=True,
)
class AssistantRequest:
    """
    Public request accepted by the
    Assistant Platform.
    """

    explanation: ExplanationSnapshot

    audience: str = "developer"

    renderer: str = "markdown"

    provider: str = "gemini"