from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Usage:
    """
    Token usage reported by a language model.
    """

    input_tokens: int = 0

    output_tokens: int = 0

    total_tokens: int = 0