from backend.operations.integration.composition import (
    OperationsIntegrationComposition,
)


def test_context_composition() -> None:
    context = (
        OperationsIntegrationComposition()
        .compose()
    )

    assert context.cases is not None

    assert context.verification is not None

    assert context.outcome is not None

    assert context.monitoring is not None

    assert context.policy is not None