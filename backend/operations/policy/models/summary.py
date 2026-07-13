from __future__ import annotations

from dataclasses import dataclass

from backend.operations.models.identifiers import (
    PolicyId,
)
from backend.operations.policy.models.decision import (
    PolicyDecision,
)


@dataclass(
    frozen=True,
    slots=True,
)
class PolicySummary:
    """
    Lightweight summary of a
    policy evaluation.
    """

    id: PolicyId

    decision: PolicyDecision