from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class PolicyRule:
    """
    Policy rule evaluated against
    monitoring findings.
    """

    name: str

    threshold: float

    description: str