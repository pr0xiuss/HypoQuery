from __future__ import annotations

from dataclasses import dataclass

from backend.knowledge.models.explanation_snapshot import (
    ExplanationSnapshot,
)


@dataclass(frozen=True, slots=True)
class AssistantJob:
    """
    Represents one assistant request.

    An AssistantJob transforms an ExplanationSnapshot
    into an AI-generated response.
    """

    explanation: ExplanationSnapshot