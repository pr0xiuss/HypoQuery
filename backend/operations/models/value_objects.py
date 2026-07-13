from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class ConfidenceScore:
    """
    Confidence associated with an Operational Assessment.

    Value is expected to be within the range [0.0, 1.0].
    Validation is performed by the Assessment domain,
    not by this value object.
    """

    value: float

