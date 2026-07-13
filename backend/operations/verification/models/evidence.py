from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(
    frozen=True,
    slots=True,
)
class VerificationEvidence:
    """
    Technical evidence collected during
    verification.
    """

    execution_plan_changed: bool

    planner_changed: bool

    metrics: dict[str, float] = field(
        default_factory=dict,
    )