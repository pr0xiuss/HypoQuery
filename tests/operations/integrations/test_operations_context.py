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


def test_operations_context() -> None:
    context = OperationsIntegrationContext(
        cases=CaseComposition().compose(),
        verification=VerificationComposition().compose(),
        outcome=OutcomeComposition().compose(),
        monitoring=MonitoringComposition().compose(),
        policy=PolicyComposition().compose(),
    )

    assert context.cases is not None
    assert context.verification is not None
    assert context.outcome is not None
    assert context.monitoring is not None
    assert context.policy is not None