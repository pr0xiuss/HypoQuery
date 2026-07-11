from __future__ import annotations

from dataclasses import dataclass

from backend.assistant.models.prompt import (
    Prompt,
)


@dataclass(frozen=True, slots=True)
class AIRequest:
    """
    Request submitted to a language model.
    """

    prompt: Prompt

    temperature: float = 0.2

    max_tokens: int = 1024