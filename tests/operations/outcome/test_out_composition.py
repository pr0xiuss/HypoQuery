from backend.operations.outcome.composition import (
    OutcomeComposition,
)
from backend.operations.outcome.context import (
    OutcomeContext,
)


def test_outcome_composition_creates_context() -> None:
    composition = OutcomeComposition()

    context = composition.compose()

    assert isinstance(
        context,
        OutcomeContext,
    )