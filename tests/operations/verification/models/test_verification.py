from uuid import uuid4

from backend.operations.models.identifiers import (
    VerificationId,
)
from backend.operations.models.references import (
    RecommendationReference,
)
from backend.operations.verification.models.comparison import (
    VerificationComparison,
)
from backend.operations.verification.models.evidence import (
    VerificationEvidence,
)
from backend.operations.verification.models.verification import (
    Verification,
)
from backend.optimization.recommendation.models.recommendation_key import (
    RecommendationKey,
)


def test_verification() -> None:
    recommendation = RecommendationReference(
        key=RecommendationKey(
            category="INDEX",
            target="orders(customer_id)",
            action="CREATE",
        ),
        recommendation_code="CREATE_INDEX",
    )

    comparison = VerificationComparison(
        expected="Index Scan",
        observed="Index Scan",
        matches=True,
    )

    evidence = VerificationEvidence(
        execution_plan_changed=True,
        planner_changed=True,
    )

    verification = Verification(
        id=VerificationId(uuid4()),
        recommendation=recommendation,
        comparison=comparison,
        evidence=evidence,
    )

    assert verification.comparison.matches
    assert verification.evidence.execution_plan_changed
    assert verification.recommendation == recommendation