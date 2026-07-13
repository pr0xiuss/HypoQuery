from backend.operations.cases.composition import (
    CaseComposition,
)
from backend.operations.cases.context import (
    CaseContext,
)


def test_case_composition_creates_context() -> None:
    composition = CaseComposition()

    context = composition.compose()

    assert isinstance(
        context,
        CaseContext,
    )