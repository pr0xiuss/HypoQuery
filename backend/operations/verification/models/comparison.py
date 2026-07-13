from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class VerificationComparison:
    """
    Deterministic comparison between the
    expected optimization state and the
    observed database state.
    """

    expected: str

    observed: str

    matches: bool