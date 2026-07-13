from uuid import uuid4

from backend.operations.models.identifiers import (
    VerificationId,
)
from backend.operations.models.references import (
    RecommendationReference,
)
from backend.operations.verification.engine import (
    VerificationEngine,
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


def test_engine_creates_verification() -> None:
    repository = MemoryVerificationRepository()

    engine = VerificationEngine(
        repository=repository,
    )

    verification = build_verification()

    engine.create(
        verification,
    )

    assert engine.contains(
        verification.id,
    )


def test_engine_finds_verification() -> None:
    repository = MemoryVerificationRepository()

    engine = VerificationEngine(
        repository=repository,
    )

    verification = build_verification()

    engine.create(
        verification,
    )

    assert (
        engine.find(
            verification.id,
        )
        == verification
    )