from uuid import uuid4

from backend.operations.cases.composition import (
    CaseComposition,
)
from backend.operations.models.enums import (
    CasePriority,
)
from backend.operations.models.references import (
    RecommendationReference,
)
from backend.operations.verification.composition import (
    VerificationComposition,
)
from backend.operations.verification.models.comparison import (
    VerificationComparison,
)
from backend.optimization.recommendation.models.recommendation_key import (
    RecommendationKey,
)
from backend.operations.cases.models.recommendation_reference_collection import (
    RecommendationReferenceCollection,
)
from backend.operations.cases.models.metadata import (
    CaseMetadata,
)
from backend.operations.models.enums import (
    CaseIntent,
)
from backend.operations.models.references import (
    RecommendationReference,
)
from backend.optimization.recommendation.models.recommendation_key import (
    RecommendationKey,
)
from backend.operations.verification.models.evidence import VerificationEvidence

def test_case_to_verification() -> None:
    case_context = (
        CaseComposition()
        .compose()
    )

    verification_context = (
        VerificationComposition()
        .compose()
    )

    recommendation = RecommendationReference(
        key=RecommendationKey(
            category="INDEX",
            target="users.email",
            action="CREATE",
        ),
        recommendation_code="IDX_USERS_EMAIL",
        recommendation_version=1,
    )

    case = case_context.service.create(
        recommendations=RecommendationReferenceCollection(
            recommendations=[
                recommendation,
            ],
        ),
        metadata=CaseMetadata(
            intent=CaseIntent.PERFORMANCE,
            labels=[
                "phase6",
                "integration",
            ],
        ),
        priority=CasePriority.HIGH,
    )

    verification = verification_context.service.create(
        recommendation=recommendation,
        comparison=VerificationComparison(
            expected="INDEX users(email)",
            observed="INDEX users(email)",
            matches=True,
        ),
        evidence=VerificationEvidence(
            execution_plan_changed=True,
            planner_changed=True,
            metrics={
                "execution_time": 95.0,
            },
        ),
    )

    assert case is not None
    assert verification.verified