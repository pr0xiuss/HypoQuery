from __future__ import annotations

from uuid import uuid4

from backend.operations.contracts.snapshots import (
    PolicySnapshot,
)
from backend.operations.models.identifiers import (
    PolicyId,
)
from backend.operations.monitoring.models.summary import (
    MonitoringSummary,
)
from backend.operations.policy.builders.policy_builder import (
    PolicyBuilder,
)
from backend.operations.policy.engine import (
    PolicyEngine,
)
from backend.operations.policy.models.decision import (
    PolicyDecision,
)
from backend.operations.policy.models.rule import (
    PolicyRule,
)


class PolicyService:
    """
    Application service for
    Policy operations.
    """

    def __init__(
        self,
        engine: PolicyEngine,
        builder: PolicyBuilder,
    ) -> None:
        self._engine = engine
        self._builder = builder

    def create(
        self,
        *,
        monitoring: MonitoringSummary,
        rule: PolicyRule,
        decision: PolicyDecision,
    ) -> PolicySnapshot:

        policy = (
            self._builder
            .with_id(
                PolicyId(
                    uuid4(),
                )
            )
            .with_monitoring(
                monitoring,
            )
            .with_rule(
                rule,
            )
            .with_decision(
                decision,
            )
            .build()
        )

        self._engine.create(
            policy,
        )

        return PolicySnapshot(
            policy_id=policy.id,
            decision=policy.decision,
        )