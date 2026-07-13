from __future__ import annotations

from dataclasses import dataclass

from backend.operations.models.identifiers import (
    PolicyId,
)
from backend.operations.monitoring.models.summary import (
    MonitoringSummary,
)
from backend.operations.policy.models.decision import (
    PolicyDecision,
)
from backend.operations.policy.models.rule import (
    PolicyRule,
)


@dataclass(
    slots=True,
)
class Policy:
    """
    Aggregate representing evaluation
    of monitoring findings against
    operational policy.
    """

    id: PolicyId

    monitoring: MonitoringSummary

    rule: PolicyRule

    decision: PolicyDecision