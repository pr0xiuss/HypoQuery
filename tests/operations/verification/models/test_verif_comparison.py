from backend.operations.verification.models.comparison import (
    VerificationComparison,
)


def test_verification_comparison() -> None:
    comparison = VerificationComparison(
        expected="Index Scan",
        observed="Index Scan",
        matches=True,
    )

    assert comparison.expected == "Index Scan"
    assert comparison.observed == "Index Scan"
    assert comparison.matches