from backend.operations.integration.composition import (
    OperationsIntegrationComposition,
)
from backend.operations.integration.context import (
    OperationsIntegrationContext,
)


def test_operations_composition() -> None:
    composition = OperationsIntegrationComposition()

    context = composition.compose()

    assert isinstance(
        context,
        OperationsIntegrationContext,
    )