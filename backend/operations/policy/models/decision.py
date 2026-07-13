from __future__ import annotations

from dataclasses import dataclass

from backend.operations.models.enums import (
    PolicyDecisionType,
)


@dataclass(
    frozen=True,
    slots=True,
)
class PolicyDecision:
    """
    Decision produced after evaluating
    monitoring findings against policy.
    """

    decision: PolicyDecisionType

    confidence: float

    summary: str