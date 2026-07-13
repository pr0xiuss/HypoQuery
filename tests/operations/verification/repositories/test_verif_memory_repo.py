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
from backend.operations.verification.repositories.memory_repository import (
    MemoryVerificationRepository,
)
from backend.optimization.recommendation.models.recommendation_key import (
    RecommendationKey,
)


def build_verification() -> Verification:
    recommendation = RecommendationReference(
        key=RecommendationKey(
            category="INDEX",
            target="orders(customer_id)",
            action="CREATE",
        ),
        recommendation_code="CREATE_INDEX",
    )

    return Verification(
        id=VerificationId(uuid4()),
        recommendation=recommendation,
        comparison=VerificationComparison(
            expected="Index Scan",
            observed="Index Scan",
            matches=True,
        ),
        evidence=VerificationEvidence(
            execution_plan_changed=True,
            planner_changed=True,
        ),
    )


def test_add_verification() -> None:
    repository = MemoryVerificationRepository()

    verification = build_verification()

    repository.add(
        verification,
    )

    assert repository.contains(
        verification.id,
    )


def test_find_verification() -> None:
    repository = MemoryVerificationRepository()

    verification = build_verification()

    repository.add(
        verification,
    )

    assert (
        repository.find(
            verification.id,
        )
        == verification
    )


def test_find_unknown_verification_returns_none() -> None:
    repository = MemoryVerificationRepository()

    assert (
        repository.find(
            VerificationId(uuid4()),
        )
        is None
    )