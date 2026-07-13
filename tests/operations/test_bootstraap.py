from backend.operations.bootstrap import (
    bootstrap_operations,
)
from backend.operations.composition.operations_composition import (
    OperationsComposition,
)


def test_bootstrap_returns_operations_composition() -> None:
    composition = bootstrap_operations()

    assert isinstance(
        composition,
        OperationsComposition,
    )