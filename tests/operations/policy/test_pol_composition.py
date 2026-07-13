from backend.operations.policy.composition import (
    PolicyComposition,
)
from backend.operations.policy.context import (
    PolicyContext,
)


def test_policy_composition_creates_context() -> None:
    composition = PolicyComposition()

    context = composition.compose()

    assert isinstance(
        context,
        PolicyContext,
    )