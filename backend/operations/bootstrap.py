from __future__ import annotations

from backend.operations.composition.operations_composition import (
    OperationsComposition,
)


def bootstrap_operations() -> OperationsComposition:
    """
    Bootstrap the Operations bounded context.
    """

    return OperationsComposition()