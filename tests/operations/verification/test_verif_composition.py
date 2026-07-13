from backend.operations.verification.composition import (
    VerificationComposition,
)
from backend.operations.verification.context import (
    VerificationContext,
)


def test_verification_composition_creates_context() -> None:
    composition = VerificationComposition()

    context = composition.compose()

    assert isinstance(
        context,
        VerificationContext,
    )