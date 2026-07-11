from __future__ import annotations

from dataclasses import dataclass

from backend.assistant.models.usage import (
    Usage,
)


@dataclass(frozen=True, slots=True)
class AIResponse:
    """
    Response returned by a language model.
    """

    content: str

    model: str

    usage: Usage