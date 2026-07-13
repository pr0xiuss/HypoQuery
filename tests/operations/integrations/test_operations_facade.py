from backend.operations.facade.operations_facade import (
    OperationsFacade,
)
from backend.operations.integration.composition import (
    OperationsIntegrationComposition,
)


def test_operations_facade() -> None:
    context = (
        OperationsIntegrationComposition()
        .compose()
    )

    facade = OperationsFacade(
        context=context,
    )

    assert facade.cases is context.cases.service
    assert (
        facade.verification
        is context.verification.service
    )
    assert (
        facade.outcome
        is context.outcome.service
    )
    assert (
        facade.monitoring
        is context.monitoring.service
    )
    assert (
        facade.policy
        is context.policy.service
    )