from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RetrievalScore:
    """
    Represents the ranking score assigned to one piece
    of retrieved evidence.

    Ranking is performed after deterministic retrieval.
    """

    confidence: float

    relevance: float

    total: float