from __future__ import annotations

from backend.operations.cases.composition import (
    CaseComposition,
)
from backend.operations.integration.context import (
    OperationsIntegrationContext,
)
from backend.operations.monitoring.composition import (
    MonitoringComposition,
)
from backend.operations.outcome.composition import (
    OutcomeComposition,
)
from backend.operations.policy.composition import (
    PolicyComposition,
)
from backend.operations.verification.composition import (
    VerificationComposition,
)


class OperationsIntegrationComposition:
    """
    Composition root for the
    Operations platform.
    """

    def compose(
        self,
    ) -> OperationsIntegrationContext:
        return OperationsIntegrationContext(
            cases=CaseComposition().compose(),
            verification=VerificationComposition().compose(),
            outcome=OutcomeComposition().compose(),
            monitoring=MonitoringComposition().compose(),
            policy=PolicyComposition().compose(),
        )