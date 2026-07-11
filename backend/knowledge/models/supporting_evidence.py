from __future__ import annotations

from dataclasses import dataclass

from backend.knowledge.retrieval.evidence.evidence import (
    Evidence,
)


@dataclass(frozen=True, slots=True)
class SupportingEvidence:
    """
    Represents evidence included in an optimization
    context as supporting information.

    Supporting evidence complements the primary
    reasoning without being the central focus.
    """

    evidence: Evidence

    explanation: str = ""