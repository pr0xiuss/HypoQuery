from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class OutcomeAssessment:
    """
    Engineering assessment of an
    optimization outcome.
    """

    category: str

    confidence: float

    summary: str