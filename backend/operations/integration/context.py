from __future__ import annotations

from backend.operations.cases.context import (
    CaseContext,
)
from backend.operations.monitoring.context import (
    MonitoringContext,
)
from backend.operations.outcome.context import (
    OutcomeContext,
)
from backend.operations.policy.context import (
    PolicyContext,
)
from backend.operations.verification.context import (
    VerificationContext,
)


class OperationsIntegrationContext:
    """
    Runtime integration context for the
    Operations platform.
    """

    def __init__(
        self,
        *,
        cases: CaseContext,
        verification: VerificationContext,
        outcome: OutcomeContext,
        monitoring: MonitoringContext,
        policy: PolicyContext,
    ) -> None:
        self._cases = cases
        self._verification = verification
        self._outcome = outcome
        self._monitoring = monitoring
        self._policy = policy

    @property
    def cases(
        self,
    ) -> CaseContext:
        return self._cases

    @property
    def verification(
        self,
    ) -> VerificationContext:
        return self._verification

    @property
    def outcome(
        self,
    ) -> OutcomeContext:
        return self._outcome

    @property
    def monitoring(
        self,
    ) -> MonitoringContext:
        return self._monitoring

    @property
    def policy(
        self,
    ) -> PolicyContext:
        return self._policy