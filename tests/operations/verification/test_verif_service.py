from backend.operations.models.references import (
    RecommendationReference,
)
from backend.operations.verification.builders.verification_builder import (
    VerificationBuilder,
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
from backend.operations.verification.repositories.memory_repository import (
    MemoryVerificationRepository,
)
from backend.operations.verification.service import (
    VerificationService,
)
from backend.optimization.recommendation.models.recommendation_key import (
    RecommendationKey,
)


def build_recommendation() -> RecommendationReference:
    return RecommendationReference(
        key=RecommendationKey(
            category="INDEX",
            target="orders(customer_id)",
            action="CREATE",
        ),
        recommendation_code="CREATE_INDEX",
    )


def test_service_creates_verification_snapshot() -> None:
    repository = MemoryVerificationRepository()

    service = VerificationService(
        engine=VerificationEngine(
            repository,
        ),
        builder=VerificationBuilder(),
    )

    snapshot = service.create(
        recommendation=build_recommendation(),
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

    assert snapshot.verified