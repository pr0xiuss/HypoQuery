from __future__ import annotations

from backend.operations.models.identifiers import (
    PolicyId,
)
from backend.operations.monitoring.models.summary import (
    MonitoringSummary,
)
from backend.operations.policy.models.decision import (
    PolicyDecision,
)
from backend.operations.policy.models.policy import (
    Policy,
)
from backend.operations.policy.models.rule import (
    PolicyRule,
)


class PolicyBuilder:
    """
    Fluent builder for constructing
    Policy aggregates.
    """

    def __init__(self) -> None:
        self._id: PolicyId | None = None
        self._monitoring: MonitoringSummary | None = None
        self._rule: PolicyRule | None = None
        self._decision: PolicyDecision | None = None

    def with_id(
        self,
        identifier: PolicyId,
    ) -> "PolicyBuilder":
        self._id = identifier
        return self

    def with_monitoring(
        self,
        monitoring: MonitoringSummary,
    ) -> "PolicyBuilder":
        self._monitoring = monitoring
        return self

    def with_rule(
        self,
        rule: PolicyRule,
    ) -> "PolicyBuilder":
        self._rule = rule
        return self

    def with_decision(
        self,
        decision: PolicyDecision,
    ) -> "PolicyBuilder":
        self._decision = decision
        return self

    def build(self) -> Policy:
        if self._id is None:
            raise ValueError(
                "Policy identifier is required."
            )

        if self._monitoring is None:
            raise ValueError(
                "Monitoring summary is required."
            )

        if self._rule is None:
            raise ValueError(
                "Policy rule is required."
            )

        if self._decision is None:
            raise ValueError(
                "Policy decision is required."
            )

        return Policy(
            id=self._id,
            monitoring=self._monitoring,
            rule=self._rule,
            decision=self._decision,
        )