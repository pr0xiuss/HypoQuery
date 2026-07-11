from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ExplanationSummary:
    """
    High-level summary describing the generated
    explanation.

    The summary provides a concise overview before
    consumers inspect individual explanation sections.
    """

    title: str = ""

    overview: str = ""

    confidence: float = 0.0